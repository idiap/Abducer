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
"""Import the 2026-07-21 Yang--Mills bundle without conflating source and capability.

The archive has three different roles in Abducer.  Its bytes and package
checksums are immutable provenance; its filtered snapshot is read-only replay
material; and a much smaller set of normalized records is target evidence.
Keeping those roles separate prevents generated papers, cache files, and an
upstream skill installer from silently becoming active discovery operators.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from agentic_common import ROOT, rel, utc_now, write_json
from agentic.discovery.contracts import canonical_digest, stable_identifier, validate_payload
from agentic.discovery.literature import (
    LANE_TYPES,
    assimilate_literature,
    validate_assimilation,
    validate_snapshot,
)


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
VERSION = "2026-07-21"
EXPECTED_ARCHIVE_SHA256 = "d34b5daca880bed58e2fa908d7dbaa137c55b9f1980b89dcdc26498528e7492f"
EXPECTED_CHECKSUM_COUNT = 1389

IMPORT_ROOT = ROOT / "agentic/external/yang_mills_representational_dynamics" / VERSION
ARCHIVE_ROOT = IMPORT_ROOT / "source_archives"
DEFAULT_ARCHIVE = ARCHIVE_ROOT / "full ym_representational_dynamics_complete_2026-07-21 (1).zip"
SNAPSHOT_ROOT = IMPORT_ROOT / "active_snapshot"
NORMALIZED_ROOT = IMPORT_ROOT / "normalized"
REPORT_ROOT = ROOT / "agentic/reports/ym_representational_dynamics_integration" / VERSION
REGISTERED_RUNTIME_ROOT = REPORT_ROOT / "canonical_parent_cycle"
EVAL_ROOT = ROOT / "agentic/evals/ym_representational_dynamics_20260721"
DEFAULT_LITERATURE = EVAL_ROOT / "literature_snapshot_current.json"
YM_REGISTRY = ROOT / "agentic/registries/ym_representational_dynamics_20260721.yaml"
OLD_IMPORT_ROOT = ROOT / "agentic/external/yang_mills_representational_dynamics/2026-07-20"
CANONICAL_LITERATURE_SNAPSHOT = NORMALIZED_ROOT / "canonical_target_literature_snapshot.json"
CANONICAL_LITERATURE_ASSIMILATION = NORMALIZED_ROOT / "canonical_literature_assimilation_packet.json"
BROAD_FRONTIER_CAPTURE = EVAL_ROOT / "frontier_search_live_capture_20260721.json"
DIRECT_CLAIM_MAPPING_EXPECTATIONS = (
    EVAL_ROOT / "direct_challenger_claim_mapping_expectations_20260721.json"
)
INCUMBENT_OVERLAP_EXPECTATIONS = (
    EVAL_ROOT / "incumbent_overlap_expectations_20260721.json"
)
INCUMBENT_OVERLAP_EVALUATION = NORMALIZED_ROOT / "incumbent_overlap_evaluation.json"
REGISTERED_RUNTIME_BINDING = NORMALIZED_ROOT / "registered_canonical_runtime_binding.json"

# The first portfolio materialization is the earliest durable timestamp for the
# intuition text.  It is intentionally weaker than an assertion about when the
# ideas first occurred.  The later provider-backed repair can therefore prove
# only that it preserved these strings before adding its new source mappings.
PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT = "2026-07-21T21:33:36+02:00"
PROVIDER_REBASE_RECORDED_AT = "2026-07-21T21:44:17+02:00"
DIRECT_CHALLENGER_ID = "arxiv-2606.19362"
RIVAL_GENERATOR_IDENTITY = "ym21-aggressive-rival-generator-v2"
LANE_GENEALOGY_SOURCE_IDS = frozenset(
    {
        "arxiv-2503.03060",
        "arxiv-2201.03487",
        "arxiv-2006.04987",
        "arxiv-1412.5148",
        "arxiv-1703.00501",
        "arxiv-1906.00999",
        "arxiv-1410.0664",
    }
)

ACTIVE_NEW_SKILLS = (
    "ym-prove-adaptive-block-domination",
    "ym-prove-state-weighted-defect-transfer",
    "ym-prove-conditional-partition-ratio",
)
PUBLICATION_SKILLS = (
    "ym-develop-paper-proofs",
    "ym-ground-paper-literature",
    "ym-frame-paper-narrative",
    "ym-build-proof-appendix",
    "ym-build-latex-paper",
    "ym-draft-frustration-obstruction",
    "ym-draft-finite-block-certificate",
    "ym-draft-representational-dynamics",
    "ym-draft-heat-kernel-enclosures",
    "ym-draft-staple-dispersion",
)
REUSED_SKILLS = (
    "ym-freeze-clay-target",
    "ym-build-observable-core",
    "ym-build-representation-calculus",
    "ym-define-relational-rigidity",
    "ym-design-regulator-atlas",
    "ym-build-gauge-covariant-rg",
    "ym-design-infrared-basin",
    "ym-control-large-fields-and-topology",
    "ym-prove-basin-entry",
    "ym-prove-rg-to-rigidity",
    "ym-prove-continuum-coherence",
    "ym-prove-rigidity-transfer",
    "ym-reconstruct-os-gap",
    "ym-calibrate-restricted-models",
    "ym-mechanize-proof-core",
    "ym-audit-frontier",
    "ym-run-clay-program",
)

EXCLUDED_DIRECTORY_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
}
EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".zip",
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".bbl",
    ".blg",
}
MAX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_MEMBER_BYTES = 128 * 1024 * 1024


class IntegrationError(RuntimeError):
    """Raised when an immutable or epistemic integration invariant fails."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def tree_digest(root: Path) -> str:
    """Hash a tree by relative path and content, independent of mtimes/modes."""

    rows: list[tuple[str, int, str]] = []
    if root.exists():
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            rows.append((path.relative_to(root).as_posix(), path.stat().st_size, sha256_file(path)))
    return sha256_bytes(canonical_bytes(rows))


def _safe_member_path(raw_name: str) -> PurePosixPath:
    """Normalize one zip name and reject every ambiguous filesystem escape."""

    if not raw_name or "\\" in raw_name or raw_name.startswith("/"):
        raise IntegrationError(f"unsafe archive member: {raw_name!r}")
    path = PurePosixPath(raw_name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise IntegrationError(f"unsafe archive member: {raw_name!r}")
    if path.parts and re.match(r"^[A-Za-z]:$", path.parts[0]):
        raise IntegrationError(f"drive-qualified archive member: {raw_name!r}")
    return path


def safe_file_members(archive: zipfile.ZipFile) -> list[tuple[zipfile.ZipInfo, PurePosixPath]]:
    """Return validated regular-file members with zip-bomb and duplicate guards."""

    rows: list[tuple[zipfile.ZipInfo, PurePosixPath]] = []
    seen: set[str] = set()
    total = 0
    for info in archive.infolist():
        if info.is_dir():
            continue
        path = _safe_member_path(info.filename)
        normalized = path.as_posix()
        if normalized in seen:
            raise IntegrationError(f"duplicate archive member: {normalized}")
        seen.add(normalized)
        unix_mode = (info.external_attr >> 16) & 0xFFFF
        if unix_mode and stat.S_ISLNK(unix_mode):
            raise IntegrationError(f"symbolic links are forbidden in source archives: {normalized}")
        if info.file_size > MAX_MEMBER_BYTES:
            raise IntegrationError(f"archive member exceeds size limit: {normalized}")
        total += info.file_size
        if total > MAX_UNCOMPRESSED_BYTES:
            raise IntegrationError("archive exceeds uncompressed-size limit")
        rows.append((info, path))
    return rows


def exclusion_reason(path: PurePosixPath) -> str | None:
    """Identify non-source byproducts that never enter the active snapshot/index."""

    if any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts):
        return "cache_or_build_directory"
    lower = path.name.lower()
    if lower.endswith(".synctex.gz"):
        return "latex_build_byproduct"
    suffix = Path(lower).suffix
    if suffix in EXCLUDED_SUFFIXES:
        if suffix == ".zip":
            return "nested_archive"
        if suffix in {".pyc", ".pyo"}:
            return "compiled_python_cache"
        return "build_byproduct"
    return None


def classify_active_path(path: PurePosixPath) -> str:
    """Classify imported bytes without automatically activating them."""

    relative = path.as_posix()
    skill_match = re.search(r"/\.agents/skills/([^/]+)/SKILL\.md$", relative)
    if skill_match:
        name = skill_match.group(1)
        if name in ACTIVE_NEW_SKILLS:
            return "activated_skill_source"
        if name in PUBLICATION_SKILLS:
            return "external_only_publication_skill"
        return "external_reference_skill"
    if relative.startswith("51_publication_portfolio/"):
        return "external_only_publication_artifact"
    if path.name.startswith("test_") and path.suffix == ".py":
        return "stage_replay_test"
    if path.suffix == ".py":
        return "stage_replay_code"
    if path.suffix in {".json", ".md", ".tex", ".pdf", ".sha256"}:
        return "evidence_only"
    return "preserved_source_support"


def verify_package_checksums(
    archive: zipfile.ZipFile,
    members: dict[str, zipfile.ZipInfo],
) -> dict[str, Any]:
    """Verify the upstream checksum manifest directly against raw zip bytes."""

    checksum_name = "CHECKSUMS.sha256"
    if checksum_name not in members:
        raise IntegrationError("archive has no CHECKSUMS.sha256")
    checksum_payload = archive.read(members[checksum_name])
    failures: list[dict[str, str]] = []
    verified = 0
    paths: list[str] = []
    for raw_line in checksum_payload.decode("utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line)
        if not match:
            failures.append({"path": "", "reason": f"unparseable:{line}"})
            continue
        expected, raw_path = match.groups()
        normalized = _safe_member_path(raw_path.removeprefix("./")).as_posix()
        paths.append(normalized)
        info = members.get(normalized)
        if info is None:
            failures.append({"path": normalized, "reason": "missing"})
            continue
        actual = sha256_bytes(archive.read(info))
        if actual != expected.lower():
            failures.append({"path": normalized, "reason": f"hash:{actual}"})
            continue
        verified += 1
    if len(paths) != len(set(paths)):
        raise IntegrationError("upstream checksum manifest contains duplicate paths")
    return {
        "schema_version": 1,
        "checksum_file": checksum_name,
        "checksum_manifest_sha256": sha256_bytes(checksum_payload),
        "declared_count": len(paths),
        "verified_count": verified,
        "failed_count": len(failures),
        "all_ok": not failures,
        "failures": failures,
    }


def _copy_raw_once(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if sha256_file(destination) != EXPECTED_ARCHIVE_SHA256:
            raise IntegrationError(f"immutable raw archive changed: {rel(destination)}")
        return
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".archive-", delete=False) as handle:
        temp_path = Path(handle.name)
        with source.open("rb") as incoming:
            shutil.copyfileobj(incoming, handle, length=1024 * 1024)
    try:
        if sha256_file(temp_path) != EXPECTED_ARCHIVE_SHA256:
            raise IntegrationError("copied archive digest changed")
        os.replace(temp_path, destination)
        destination.chmod(0o444)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _make_tree_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    root.chmod(0o555)


def _verify_existing_snapshot(expected: list[dict[str, Any]]) -> None:
    actual_paths = {
        path.relative_to(SNAPSHOT_ROOT).as_posix()
        for path in SNAPSHOT_ROOT.rglob("*")
        if path.is_file()
    }
    expected_paths = {row["path"] for row in expected}
    if actual_paths != expected_paths:
        extra = sorted(actual_paths - expected_paths)[:10]
        missing = sorted(expected_paths - actual_paths)[:10]
        raise IntegrationError(f"immutable snapshot path drift; extra={extra}, missing={missing}")
    for row in expected:
        path = SNAPSHOT_ROOT / row["path"]
        if path.stat().st_size != row["size_bytes"] or sha256_file(path) != row["sha256"]:
            raise IntegrationError(f"immutable snapshot content drift: {row['path']}")


def extract_snapshot(
    archive: zipfile.ZipFile,
    rows: list[tuple[zipfile.ZipInfo, PurePosixPath]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Materialize the filtered snapshot atomically, or verify the prior copy."""

    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for info, path in rows:
        reason = exclusion_reason(path)
        if reason:
            excluded.append({"path": path.as_posix(), "reason": reason, "size_bytes": info.file_size})
            continue
        payload = archive.read(info)
        included.append(
            {
                "path": path.as_posix(),
                "size_bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "disposition": classify_active_path(path),
            }
        )
    included.sort(key=lambda row: row["path"])
    excluded.sort(key=lambda row: row["path"])

    if SNAPSHOT_ROOT.exists():
        _verify_existing_snapshot(included)
        return included, excluded

    IMPORT_ROOT.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=".active-snapshot-", dir=IMPORT_ROOT))
    try:
        info_by_name = {_safe_member_path(info.filename).as_posix(): info for info, _ in rows}
        for row in included:
            destination = temp_root / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(info_by_name[row["path"]]))
        os.replace(temp_root, SNAPSHOT_ROOT)
        _make_tree_read_only(SNAPSHOT_ROOT)
    finally:
        if temp_root.exists():
            shutil.rmtree(temp_root)
    _verify_existing_snapshot(included)
    return included, excluded


def _write_immutable_json(path: Path, payload: Any) -> str:
    """Write a canonical source artifact once and lock its digest."""

    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if path.exists():
        if path.read_text(encoding="utf-8") != rendered:
            raise IntegrationError(f"immutable manifest drift: {rel(path)}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        path.chmod(0o444)
    digest = sha256_bytes(rendered.encode("utf-8"))
    lock_path = path.with_suffix(path.suffix + ".sha256")
    lock_text = f"{digest}  {path.name}\n"
    if lock_path.exists() and lock_path.read_text(encoding="utf-8") != lock_text:
        raise IntegrationError(f"immutable manifest lock drift: {rel(lock_path)}")
    if not lock_path.exists():
        lock_path.write_text(lock_text, encoding="utf-8")
        lock_path.chmod(0o444)
    return digest


def source_reference(relative: str, index: dict[str, dict[str, Any]]) -> dict[str, str]:
    row = index.get(relative)
    if row is None:
        raise IntegrationError(f"normalization source is absent from active snapshot: {relative}")
    return {
        "source_path": f"{rel(SNAPSHOT_ROOT)}/{relative}",
        "source_sha256": row["sha256"],
    }


def validate_literature_snapshot(payload: dict[str, Any], *, require_after: str | None = None) -> None:
    """Validate the bounded external-provider capture without laundering authority.

    This dated packet records real web retrieval, but it is not an executable
    operator receipt or a systematic review.  The conservative canonical
    projection below therefore emits ``local_only`` provenance until a central
    search operator independently receipts the same sources and queries.
    """

    if payload.get("target_id") != TARGET_ID:
        raise IntegrationError("literature snapshot target mismatch")
    if payload.get("schema_version") != 2:
        raise IntegrationError("provider-backed literature snapshot schema version mismatch")
    if (
        payload.get("snapshot_kind") != "provider_backed_web_capture"
        or payload.get("provider_backed") is not True
        or payload.get("live_recency_claim") is not True
    ):
        raise IntegrationError("literature evidence must record the dated external-provider retrieval boundary")
    if payload.get("exhaustive_coverage_claim") is not False or payload.get("peer_validation_claim") is not False:
        raise IntegrationError("bounded retrieval cannot claim exhaustive coverage or peer validation")
    searched = dt.date.fromisoformat(str(payload.get("searched_at", ""))[:10])
    retrieved = dt.date.fromisoformat(str(payload.get("retrieved_at", ""))[:10])
    coverage = dt.date.fromisoformat(str(payload.get("coverage_cutoff", ""))[:10])
    if coverage < dt.date.fromisoformat(VERSION) or searched < coverage or retrieved < coverage:
        raise IntegrationError("literature snapshot predates the imported bundle or its own coverage cutoff")
    if require_after and coverage < dt.date.fromisoformat(require_after[:10]):
        raise IntegrationError(f"literature snapshot must cover at least {require_after}")

    providers = payload.get("providers")
    queries = payload.get("queries")
    sources = payload.get("sources")
    sessions = payload.get("retrieval_sessions")
    coverage_limits = payload.get("coverage_limits")
    if not isinstance(providers, list) or len(providers) < 2:
        raise IntegrationError("literature snapshot lacks named external providers")
    provider_ids = {
        str(row.get("provider_id"))
        for row in providers
        if isinstance(row, dict) and str(row.get("provider_id", "")).strip()
    }
    if len(provider_ids) != len(providers) or any(
        not str(row.get(key, "")).strip()
        for row in providers
        for key in ("name", "index", "retrieval_mode")
    ):
        raise IntegrationError("literature provider records are incomplete or duplicated")
    if not isinstance(queries, list) or len(queries) < 8:
        raise IntegrationError("literature snapshot lacks lane-specific exact queries")
    query_ids = {
        str(row.get("query_id"))
        for row in queries
        if isinstance(row, dict) and str(row.get("query_id", "")).strip()
    }
    if len(query_ids) != len(queries) or any(
        row.get("provider_id") not in provider_ids or not str(row.get("text", "")).strip()
        for row in queries
    ):
        raise IntegrationError("literature queries lack unique IDs or provider bindings")
    if not isinstance(sources, list) or len(sources) < 13:
        raise IntegrationError("literature snapshot lacks auditable query/source coverage")
    if not isinstance(sessions, list) or len(sessions) < 2:
        raise IntegrationError("literature snapshot lacks retrieval-session boundaries")
    if not isinstance(coverage_limits, list) or len(coverage_limits) < 4:
        raise IntegrationError("literature snapshot must state non-exhaustive coverage limits")

    source_ids = {
        str(row.get("source_id"))
        for row in sources
        if isinstance(row, dict) and str(row.get("source_id", "")).strip()
    }
    required_ids = {DIRECT_CHALLENGER_ID, *LANE_GENEALOGY_SOURCE_IDS}
    if not required_ids.issubset(source_ids):
        raise IntegrationError(f"literature snapshot lacks required challenger/genealogy sources: {sorted(required_ids - source_ids)}")
    session_source_ids = {
        str(source_id)
        for session in sessions
        if isinstance(session, dict)
        for source_id in session.get("source_ids", [])
    }
    if session_source_ids != source_ids or any(
        not str(session.get("session_id", "")).strip()
        or not str(session.get("retrieved_at", "")).strip()
        or not str(session.get("evidence_boundary", "")).strip()
        or not set(session.get("provider_ids", [])).issubset(provider_ids)
        for session in sessions
    ):
        raise IntegrationError("retrieval sessions must account for every source and named provider")

    withdrawn = [row for row in sources if isinstance(row, dict) and row.get("source_status") == "withdrawn"]
    if not withdrawn or any(row.get("disposition") != "excluded" for row in withdrawn):
        raise IntegrationError("withdrawn proof claims must appear as excluded negative controls")
    statuses = {str(row.get("disposition")) for row in sources if isinstance(row, dict)}
    if not {"included", "excluded"}.issubset(statuses):
        raise IntegrationError("literature snapshot must preserve both included and excluded sources")
    for row in sources:
        if not isinstance(row, dict):
            raise IntegrationError("literature source record must be an object")
        for key in (
            "source_id",
            "title",
            "url",
            "source_type",
            "source_status",
            "claim_status",
            "disposition",
            "effect_type",
            "provider_id",
            "index",
            "retrieved_at",
            "publication_date",
            "source_version",
            "domain",
            "transfer_boundary",
            "source_to_theory_delta",
        ):
            if not str(row.get(key, "")).strip():
                raise IntegrationError(f"literature source missing {key}")
        if row["provider_id"] not in provider_ids:
            raise IntegrationError(f"literature source has unknown provider: {row['source_id']}")
        if not isinstance(row.get("query_ids"), list) or not row["query_ids"] or not set(row["query_ids"]).issubset(query_ids):
            raise IntegrationError(f"literature source lacks exact query provenance: {row['source_id']}")
        if not isinstance(row.get("authors"), list) or not row["authors"]:
            raise IntegrationError(f"literature source lacks authorship metadata: {row['source_id']}")
        if not isinstance(row.get("reported_claims"), list) or not row["reported_claims"]:
            raise IntegrationError(f"literature source lacks a bounded claim transcription: {row['source_id']}")
        if row["effect_type"] not in {"spawn", "merge", "split", "reframe", "demote", "retire", "reprioritize", "unchanged"}:
            raise IntegrationError(f"literature source has unknown causal effect: {row['effect_type']}")

    challenger = next(row for row in sources if row["source_id"] == DIRECT_CHALLENGER_ID)
    if (
        challenger.get("source_status") != "unverified_challenger"
        or challenger.get("claim_status") != "unverified_challenger"
        or challenger.get("disposition") != "included"
    ):
        raise IntegrationError("the June 2026 direct claim must remain an included unverified challenger")
    audits = challenger.get("claim_audit")
    if not isinstance(audits, list) or len(audits) != 6:
        raise IntegrationError("the June 2026 challenger must retain exactly six claim-by-claim proof obligations")
    audit_ids = {str(row.get("claim_id")) for row in audits if isinstance(row, dict)}
    if len(audit_ids) != len(audits) or any(
        row.get("verification_status") != "unverified"
        or not str(row.get("author_stated_claim", "")).strip()
        or not str(row.get("required_obligation", "")).strip()
        for row in audits
    ):
        raise IntegrationError("the June 2026 challenger audit cannot contain accepted or unbound claims")


def validate_frontier_search_capture(payload: Mapping[str, Any]) -> None:
    """Validate the frozen broad search response and its honest receipt boundary."""

    if payload.get("schema_version") in {"2.0", "2.1"}:
        _validate_current_frontier_search_capture(payload)
        return

    if payload.get("schema_version") != "1.0" or payload.get("target_id") != TARGET_ID:
        raise IntegrationError("broad frontier capture scope or schema mismatch")
    if payload.get("capture_mode") != "live_external_web_search_frozen_for_replay":
        raise IntegrationError("broad frontier capture must preserve its external-live/frozen boundary")
    if any(
        payload.get(field) is not False
        for field in ("exhaustive_coverage_claim", "peer_validation_claim", "source_correctness_claim")
    ):
        raise IntegrationError("broad frontier capture cannot claim exhaustiveness, peer validation, or correctness")
    provider = payload.get("provider")
    if not isinstance(provider, Mapping) or (
        provider.get("receipt_status") != "externally_executed_then_frozen"
        or provider.get("executable_replay_status") != "frozen_response_adapter_only"
        or "does not pretend" not in str(provider.get("execution_boundary", ""))
    ):
        raise IntegrationError("broad frontier capture launders frozen metadata into a network replay")
    lanes = payload.get("lanes")
    results = payload.get("raw_results")
    if not isinstance(lanes, list) or not isinstance(results, list):
        raise IntegrationError("broad frontier capture lacks lane or raw-result arrays")
    if len(lanes) != len(LANE_TYPES) or {row.get("lane_type") for row in lanes} != set(LANE_TYPES):
        raise IntegrationError("broad frontier capture must execute exactly the six canonical lanes")
    lane_ids = [str(row.get("lane_id", "")) for row in lanes]
    if len(set(lane_ids)) != len(lane_ids) or any(not lane_id for lane_id in lane_ids):
        raise IntegrationError("broad frontier lane IDs are missing or duplicated")
    # These expressions catch the identifiers that would turn a frontier query
    # into a known-record lookup.  Four-digit years are intentionally allowed.
    seeded_identifier = re.compile(
        r"(?i)(arxiv\s*:|doi\s*:|abstract_id\s*=|(?:ssrn|zenodo)[- :]*(?:record[- :]*|id[- :]*)?\d{6,}|"
        r"\b\d{4}\.\d{4,5}\b|\b10\.\d{4,9}/\S+)"
    )
    referenced_ids: set[str] = set()
    for lane in lanes:
        queries = lane.get("queries")
        raw_ids = lane.get("raw_result_ids")
        if lane.get("status") != "completed" or not isinstance(queries, list) or not queries:
            raise IntegrationError(f"broad frontier lane was not completed: {lane.get('lane_id')}")
        if not isinstance(raw_ids, list) or not raw_ids:
            raise IntegrationError(f"broad frontier lane has no raw dispositions: {lane.get('lane_id')}")
        if any(not str(query).strip() or seeded_identifier.search(str(query)) for query in queries):
            raise IntegrationError(f"frontier query was empty or known-ID seeded: {lane.get('lane_id')}")
        if "no " not in str(lane.get("query_policy", "")).lower():
            raise IntegrationError(f"frontier lane lacks an explicit anti-seeding policy: {lane.get('lane_id')}")
        referenced_ids.update(str(result_id) for result_id in raw_ids)

    result_ids = [str(row.get("result_id", "")) for row in results if isinstance(row, Mapping)]
    if len(result_ids) != len(results) or len(set(result_ids)) != len(result_ids):
        raise IntegrationError("broad frontier raw-result IDs are missing or duplicated")
    if referenced_ids != set(result_ids):
        raise IntegrationError("broad frontier lane/result accounting is not closed")
    required_fields = (
        "result_id",
        "source_id",
        "title",
        "url",
        "retrieval_status",
        "disposition",
        "reason",
        "claim_status",
    )
    if any(
        not str(row.get(field, "")).strip()
        for row in results
        for field in required_fields
    ):
        raise IntegrationError("broad frontier raw result has an incomplete disposition")
    source_ids = {str(row["source_id"]) for row in results}
    required_source_ids = {
        DIRECT_CHALLENGER_ID,
        "zenodo-19614728",
        "preprints-202604.0332-v1",
        "ssrn-4819820",
        "ssrn-6004114",
        "ssrn-6141826",
        "ssrn-6614481",
        "zenodo-21068209",
        "arxiv-2204.12737",
        "arxiv-1906.00999",
        "arxiv-1410.0664",
    }
    if not required_source_ids.issubset(source_ids):
        raise IntegrationError(
            f"broad frontier capture dropped required surveillance records: {sorted(required_source_ids - source_ids)}"
        )
    by_source = {str(row["source_id"]): row for row in results}
    for source_id in (
        DIRECT_CHALLENGER_ID,
        "zenodo-19614728",
        "preprints-202604.0332-v1",
        "ssrn-4819820",
    ):
        if by_source[source_id].get("claim_status") != "unverified_challenger":
            raise IntegrationError(f"direct frontier claim was promoted: {source_id}")
    for source_id in ("ssrn-6141826", "ssrn-6614481", "zenodo-21068209"):
        if not str(by_source[source_id].get("disposition", "")).startswith("excluded_inaccessible"):
            raise IntegrationError(f"inaccessible direct claim entered assimilation: {source_id}")
    limits = payload.get("coverage_limits")
    if not isinstance(limits, list) or len(limits) < 6 or not any(
        "absence" in str(limit).lower() and "novelty" in str(limit).lower() for limit in limits
    ):
        raise IntegrationError("broad frontier capture omits non-exhaustive/novelty limits")


def _validate_current_frontier_search_capture(payload: Mapping[str, Any]) -> None:
    """Validate current single- or multi-execution capture semantics.

    Version 2.1 is intentionally weaker about who executed a request and
    stronger about what was actually observed: it records unauthenticated agent
    observations rather than presenting API metadata as one web-provider call.
    """

    try:
        validate_payload(payload, "ym_current_literature_capture.schema.json")
    except Exception as exc:
        raise IntegrationError(f"current frontier capture schema invalid: {exc}") from exc
    body = dict(payload)
    body.pop("content_digest", None)
    if payload.get("content_digest") != canonical_digest(body):
        raise IntegrationError("current frontier capture content digest mismatch")
    started = dt.datetime.fromisoformat(str(payload["capture_started_at"]).replace("Z", "+00:00"))
    completed = dt.datetime.fromisoformat(str(payload["capture_completed_at"]).replace("Z", "+00:00"))
    cutoff = dt.datetime.fromisoformat(str(payload["coverage_cutoff"]).replace("Z", "+00:00"))
    if started.tzinfo is None or completed.tzinfo is None or cutoff.tzinfo is None:
        raise IntegrationError("current frontier capture timestamps require explicit timezones")
    if started > completed or completed != cutoff:
        raise IntegrationError("current frontier capture interval and cutoff disagree")
    if payload["schema_version"] == "2.1":
        provider = payload["provider"]
        if (
            payload["capture_mode"]
            != "agent_observed_multi_execution_literature_capture_frozen_for_replay"
            or provider["provider_id"]
            != "codex-multi-execution-literature-observation"
            or provider["receipt_status"]
            != "agent_observed_unauthenticated_executions_then_frozen"
            or provider["external_authentication_status"] != "unavailable"
        ):
            raise IntegrationError(
                "current multi-execution capture overstates its external execution authority"
            )

    lanes = payload["lanes"]
    results = payload["raw_results"]
    descriptors = payload["provider_response_artifacts"]
    lane_ids = [str(row["lane_id"]) for row in lanes]
    if len(set(lane_ids)) != len(LANE_TYPES) or {
        row["lane_type"] for row in lanes
    } != set(LANE_TYPES):
        raise IntegrationError("current frontier capture must contain each canonical lane exactly once")
    if {str(row["lane_id"]) for row in descriptors} != set(lane_ids):
        raise IntegrationError("current frontier response descriptors do not close over the six lanes")
    descriptor_paths = [str(row["path"]) for row in descriptors]
    if len(descriptor_paths) != len(set(descriptor_paths)):
        raise IntegrationError("current frontier response descriptor paths are duplicated")

    seeded_identifier = re.compile(
        r"(?i)(arxiv\s*:|doi\s*:|abstract_id\s*=|(?:ssrn|zenodo)[- :]*(?:record[- :]*|id[- :]*)?\d{6,}|"
        r"\b\d{4}\.\d{4,5}\b|\b10\.\d{4,9}/\S+)"
    )
    referenced_ids: set[str] = set()
    for lane in lanes:
        query = str(lane["queries"][0])
        if not query.strip() or seeded_identifier.search(query):
            raise IntegrationError(f"current frontier query was empty or known-ID seeded: {lane['lane_id']}")
        policy = str(lane["query_policy"]).lower()
        if "no " not in policy or not any(token in policy for token in ("identifier", "record", "doi")):
            raise IntegrationError(f"current frontier lane lacks an explicit anti-seeding policy: {lane['lane_id']}")
        referenced_ids.update(str(result_id) for result_id in lane["raw_result_ids"])
    result_ids = [str(row["result_id"]) for row in results]
    if len(result_ids) != len(set(result_ids)) or referenced_ids != set(result_ids):
        raise IntegrationError("current frontier lane/result accounting is not closed")

    required_surveillance = {
        "correction",
        "supersession",
        "withdrawal",
        "bounded_lattice",
        "conceptual_genealogy",
        "adjacent_field",
        "target_mismatch",
        "authoritative_status",
        "current_review",
        "direct_claim",
    }
    observed_surveillance = {
        str(tag) for row in results for tag in row["surveillance_tags"]
    }
    if not required_surveillance.issubset(observed_surveillance):
        raise IntegrationError(
            "current frontier capture lacks required correction/negative/adjacent surveillance: "
            f"{sorted(required_surveillance - observed_surveillance)}"
        )
    for row in results:
        disposition = str(row["disposition"])
        claim_status = str(row["claim_status"])
        if disposition == "excluded_target_mismatch" and claim_status != "excluded_target_mismatch":
            raise IntegrationError("target-mismatch disposition was not preserved as an excluded claim")
        if disposition == "excluded_retracted" and claim_status != "excluded_negative_evidence":
            raise IntegrationError("retraction disposition was not preserved as negative evidence")
        if disposition.startswith("included") and claim_status.startswith("excluded"):
            raise IntegrationError("an excluded claim status entered current literature assimilation")


HYPOTHESES = (
    ("H1", "vacuum-weight duality", "same-measure transfer/Doob identity and a gap-closing counterfamily", "same-measure full-spectrum observability on a physical nonlinear kernel"),
    ("H2", "physical-length rigidity", "positive-kernel weight-equivalence and tempered-rate bookkeeping", "a uniform physical-length theorem with sublinear chart, error, and support budgets"),
    ("H3", "collective repair", "exact rational multi-star spectra and an orientation obstruction on one fixed complex", "a growing-family boundary law covering the physical bad-displacement cone"),
    ("H4", "retained topology", "an integral finite flux carrier and scalar-sector composition obstruction", "a bounded nonabelian relative/interface carrier with transgression"),
    ("H5", "information/free energy", "a restricted product partition theorem and finite numerical information certificates", "a uniform interacting physical partition ratio or quasi-factorization"),
    ("H6", "commuting-square defects", "an exact typed telescoping/recovery calculus on a rational fixture", "a nonlinear gauge-covariant square with positive stable recovery"),
    ("H7", "atlas reconstruction", "exact finite normalized gluing with hostile normalization tests", "a boundary-rooted history-uniform nonlinear SU(2) atlas"),
    ("H8", "retained-state refinement", "an exact coarsest-stable finite refinement theorem", "a physical normalized SU(2) table with controlled stable-state complexity"),
    ("H9", "temporal density", "a multiplicity-sensitive finite dense-core theorem and hidden-mode obstruction", "OS-norm density plus uniform physical-time decay on the same observable core"),
    ("H10", "observable recovery", "an exact finite Z2 quotient recovery and composition bound", "nonlinear SU(2) quotient recovery uniform in boundary, volume, and cutoff"),
)

RIVAL_SEEDS = (
    {
        "id": "YM21-R01",
        "title": "Operator-algebraic local-net route",
        "corner": "cross_field_transfer",
        "intuition": "A physical mass scale may be forced by phase-space compactness of local observable nets before any retained-state or defect description is chosen.",
        "mechanism": "Construct the pure-gauge local observable net and seek modular or nuclearity bounds whose spectral consequence survives representation and regulator changes.",
        "new": ["local_observable_net", "modular_nuclearity", "phase_space_compactness"],
        "p": 0.22, "v": 0.98, "l": 0.90, "c": 0.96,
        "value": "Would replace a privileged RG kernel with representation-independent observable-algebra structure.",
        "learning": "Would determine whether algebraic phase-space conditions are too weak or inaccessible for nonperturbative gauge theory.",
        "question": "Which cutoff-uniform local-net compactness condition has a noncircular implication to a positive physical spectral threshold?",
        "corrections": ["No constructive pure-gauge net can be obtained without assuming the desired spectrum.", "Nuclearity admits gapless countermodels with all proposed local properties."],
        "sources": [
            ("arxiv-1906.00999", "reframe", "Use homotopy AQFT as a precise linear categorical comparator, then state the missing interacting pure-gauge net and nuclearity construction."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Audit whether the challenger's claimed OS construction supplies or bypasses the proposed local-net phase-space route; no abstract-level transfer is allowed."),
        ],
        "priority": "high_priority_collision_and_nonlinear_transfer_audit",
        "revisions": [
            "Separate linear homotopy-AQFT observables from interacting local nets and mass-generating nuclearity.",
            "Compare every net, OS, and universality premise with the unverified June 2026 construction claim before investing in proof search.",
        ],
    },
    {
        "id": "YM21-R02",
        "title": "Euclidean inequality bootstrap",
        "corner": "counter_consensus",
        "intuition": "Reflection positivity plus a closed family of gauge-invariant inequalities may constrain the continuum spectrum directly, without rare-defect counting.",
        "mechanism": "Build an axiomatic bootstrap over Wilson-loop and local gauge-invariant Schwinger functions, with positivity, crossing-like consistency, and a gap-sensitive extremal functional.",
        "new": ["euclidean_positive_functional", "observable_bootstrap_cone", "gap_extremal_functional"],
        "p": 0.28, "v": 0.91, "l": 0.82, "c": 0.78,
        "value": "Could turn OS-compatible observable constraints into a direct spectral programme independent of block geometry.",
        "learning": "Would reveal whether gauge-invariant positivity constraints are spectrally discriminating or permit hidden gapless modes.",
        "question": "Can a finite-to-infinite hierarchy of reflection-positive observable inequalities exclude every zero-threshold nonvacuum spectral measure?",
        "corrections": ["A gapless positive spectral measure satisfies the complete proposed hierarchy.", "The hierarchy presupposes continuum existence or density of the desired core."],
        "sources": [
            (DIRECT_CHALLENGER_ID, "reprioritize", "The direct reflection-positivity and OS claims collide with this lane's core mechanism and require an immediate theorem-by-theorem comparison."),
            ("clay-ym-current", "demote", "Official open status prevents the challenger or the bootstrap seed from being treated as a solved route."),
            ("mondal-jhep-2023-191", "reframe", "Keep geometric curvature arguments distinct from an observable inequality bootstrap and preserve their conditional/heuristic boundary."),
        ],
        "priority": "immediate_direct_claim_collision_audit",
        "revisions": [
            "Turn the six June 2026 abstract claims into explicit comparison obligations against the proposed positivity hierarchy.",
            "Identify which bootstrap axioms are independently constructive rather than restatements of OS reconstruction or a pre-existing gap.",
        ],
    },
    {
        "id": "YM21-R03",
        "title": "Higher-form sector rigidity",
        "corner": "ontology_inversion",
        "intuition": "The gap may be a rigidity consequence of the organization of gauge-invariant sectors and generalized symmetries, not of suppression of local bad blocks.",
        "mechanism": "Formulate a continuum-compatible category of electric/magnetic higher-form sectors and seek a theorem that sector completeness plus locality imposes a positive excitation cost.",
        "new": ["higher_form_sector_category", "superselection_cost", "generalized_symmetry_completion"],
        "p": 0.20, "v": 0.94, "l": 0.86, "c": 0.88,
        "value": "Would explain the mass scale through global sector structure while preserving local observable meaning.",
        "learning": "Would clarify whether generalized symmetry data can ever determine an energy scale rather than only classify phases.",
        "question": "What additional quantitative axiom turns sector structure into a nonzero physical excitation threshold without assuming confinement?",
        "corrections": ["Topological/sector data remain compatible with scale-free dynamics.", "The quantitative axiom is equivalent to the desired gap."],
        "sources": [
            ("arxiv-1412.5148", "reframe", "Ground higher-form sectors in the established q-form symmetry, extended-operator, and anomaly framework."),
            ("arxiv-1703.00501", "split", "Use the theta=pi center/time-reversal anomaly only as a vacuum constraint; it does not prove a theta=0 mass scale."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Ask whether the claimed confinement and continuum construction preserves, assumes, or derives the sector structure required by this lane."),
        ],
        "priority": "high_priority_quantitative_sector_bridge",
        "revisions": [
            "Name the theta, center-symmetry, line/surface-operator, and vacuum assumptions separately.",
            "Supply a noncircular quantitative principle converting sector/anomaly structure into an energy scale.",
        ],
    },
    {
        "id": "YM21-R04",
        "title": "Stochastic-quantization hypocoercivity",
        "corner": "relation_process_first",
        "intuition": "A robust relaxation scale of gauge-covariant stochastic dynamics might be the primitive nonperturbative object from which Euclidean and physical decay are reconstructed.",
        "mechanism": "Construct gauge-covariant stochastic quantization, prove cutoff-uniform hypocoercivity after quotienting gauge directions, and establish a nontrivial bridge from its generator to physical Schwinger decay.",
        "new": ["gauge_quotient_diffusion", "hypocoercive_relaxation", "dynamic_to_physical_bridge"],
        "p": 0.14, "v": 0.97, "l": 0.93, "c": 0.97,
        "value": "Would replace static defect control with a process ontology and a constructive route to the Euclidean measure.",
        "learning": "Even failure would separate algorithmic/stochastic mixing from physical spectral information sharply.",
        "question": "Can a stochastic relaxation estimate be made cutoff-uniform and linked to physical-time correlations without confusing two generators?",
        "corrections": ["Fast stochastic mixing coexists with a gapless physical Hamiltonian.", "Gauge quotient or continuum limits destroy uniform hypocoercivity."],
        "sources": [
            ("arxiv-2006.04987", "reframe", "Use the two-dimensional gauge-orbit state space and Langevin process as rigorous process genealogy, never as a four-dimensional gap result."),
            ("arxiv-2201.03487", "reframe", "Use the local 3D Yang-Mills-Higgs gauge-orbit Markov process to specify the state-space and globality obligations."),
            ("arxiv-2503.03060", "reframe", "Add uniqueness of gauge-covariant renormalisation and lattice-approximation compatibility as current obligations."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Compare the process-first route to the challenger's claimed static multiscale/OS bridge without conflating stochastic and physical generators."),
        ],
        "priority": "high_priority_current_process_genealogy",
        "revisions": [
            "Prove global pure-4D dynamics and cutoff-uniform relaxation after quotienting gauge directions.",
            "Add a separate nontrivial theorem from stochastic generator decay to Euclidean and physical-time spectral information.",
        ],
        "wildcard": True,
    },
    {
        "id": "YM21-R05",
        "title": "Gauge-orbit metric concentration",
        "corner": "cross_field_transfer",
        "intuition": "Positive curvature or transport contraction on the gauge-orbit configuration space may yield physical concentration without an explicit good/bad block decomposition.",
        "mechanism": "Define a gauge-invariant metric-measure geometry and seek volume/cutoff-uniform curvature-dimension or transport inequalities strong enough to control observable correlations.",
        "new": ["gauge_orbit_metric_measure_space", "transport_contraction", "curvature_dimension_bound"],
        "p": 0.24, "v": 0.88, "l": 0.84, "c": 0.82,
        "value": "Would unify geometry, concentration, and correlation control without an exposure filtration.",
        "learning": "Would locate whether orbit singularities, topology, or continuum scaling fundamentally obstruct global concentration geometry.",
        "question": "Is there a noncircular gauge-orbit transport inequality whose constants remain physical under volume and cutoff limits?",
        "corrections": ["Orbit singularities force curvature bounds to degenerate.", "The inequality implies only configuration concentration, not temporal spectral decay."],
        "sources": [
            ("arxiv-2006.04987", "reframe", "Use the Polish two-dimensional gauge-orbit state space as a topology/metric comparator, not a curvature or gap theorem."),
            ("arxiv-2201.03487", "reframe", "Use the nonlinear 3D Yang-Mills-Higgs orbit space to expose distributional and blow-up obstacles to a physical metric geometry."),
            ("mondal-jhep-2023-191", "reframe", "Compare directly with the existing conditional/heuristic gauge-orbit curvature programme before claiming novelty."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Audit the claimed continuum exponential clustering against this route's missing volume/cutoff-uniform concentration-to-correlation theorem; do not infer a transport inequality from clustering."),
        ],
        "priority": "high_priority_continuum_clustering_collision_and_geometry_transfer",
        "revisions": [
            "Distinguish state-space metrizability from curvature-dimension or transport contraction.",
            "Prove volume/cutoff-uniform physical constants and a separate concentration-to-temporal-spectrum implication, explicitly comparing the June 2026 continuum-clustering claim.",
        ],
    },
    {
        "id": "YM21-R06",
        "title": "Resurgent constructive completion",
        "corner": "emergence_stabilization",
        "intuition": "The nonperturbative scale may become mathematically controllable through a resurgent completion of asymptotic freedom coupled to constructive axioms, rather than through real-space basin entry.",
        "mechanism": "Seek uniform Borel-Écalle control of gauge-invariant observables, identify nonperturbative sectors, and prove that the reconstructed Schwinger functions satisfy positivity and a spectral threshold.",
        "new": ["resurgent_observable_family", "nonperturbative_transseries_sector", "constructive_resummation_axioms"],
        "p": 0.10, "v": 0.99, "l": 0.91, "c": 1.00,
        "value": "Would connect asymptotic freedom to a nonperturbative physical scale without presupposing an infrared defect model.",
        "learning": "Would expose precisely which positivity, uniformity, or ambiguity barriers prevent resummation from becoming construction.",
        "question": "Can any resurgent observable family be proved uniform, reflection-positive, and theory-identifying beyond formal perturbation theory?",
        "corrections": ["Renormalon/instanton ambiguities cannot be fixed without importing nonperturbative data equivalent to the target.", "Resummed functions fail OS positivity or uniqueness."],
        "sources": [
            (DIRECT_CHALLENGER_ID, "reprioritize", "Treat the claimed weak/strong continuum identification as a direct alternative that must be audited before a resurgent completion is judged novel or necessary."),
            ("arxiv-2506.00284-withdrawn", "retire", "Use the withdrawn proof claim only as a negative control for unsupported constructive rhetoric."),
            ("clay-ym-current", "demote", "Keep the resurgent seed and the June challenger below accepted-solution status."),
        ],
        "priority": "high_risk_protected_after_direct_claim_audit",
        "revisions": [
            "Compare the proposed nonperturbative completion with the challenger's claimed weak/strong bridge and identify distinct proof content.",
            "Make OS positivity, uniqueness, ambiguity cancellation, and theory identity independently falsifiable obligations.",
        ],
        "wildcard": True,
    },
    {
        "id": "YM21-R07",
        "title": "Exact loop-space dual completion",
        "corner": "duality_completion",
        "intuition": "A positive loop- or surface-space dual theory may make the mass scale kinematic in the correct variables even if it is opaque in connection variables.",
        "mechanism": "Construct an exact, invertible, positivity-preserving duality from gauge-invariant observables to loop/surface degrees of freedom and seek a local spectral theorem there.",
        "new": ["positive_loop_space_measure", "invertible_surface_duality", "dual_local_spectrum"],
        "p": 0.13, "v": 0.98, "l": 0.92, "c": 0.98,
        "value": "Would radically change the ontology while keeping observable equivalence explicit.",
        "learning": "Would show whether nonlocality, overcompleteness, or positivity is the decisive obstruction to dual mass-gap arguments.",
        "question": "Can a loop/surface dual be exact and reflection-positive while retaining a tractable local notion of physical propagation?",
        "corrections": ["The dual map loses observables or theory identity.", "Dual locality or positivity fails in the continuum-relevant regime."],
        "sources": [
            ("arxiv-1412.5148", "reframe", "Ground loop and surface degrees of freedom in generalized-symmetry language while keeping exact duality as an additional obligation."),
            ("arxiv-1703.00501", "split", "Use center/anomaly constraints to test sector preservation, not to infer an exact dual or a gap."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Check the challenger's claimed Wilson-loop area law and universality against this lane's demanded invertible positivity-preserving duality."),
        ],
        "priority": "high_priority_loop_claim_collision",
        "revisions": [
            "Separate generalized-symmetry classification from an invertible observable-complete loop/surface dual.",
            "Audit whether the June 2026 area-law claim supplies usable estimates or merely restates the desired continuum transfer.",
        ],
        "wildcard": True,
    },
    {
        "id": "YM21-R08",
        "title": "Direct Hamiltonian spectral-flow construction",
        "corner": "scale_regime_reversal",
        "intuition": "Instead of deriving a gap after continuum Euclidean control, one might construct a compatible family of finite-volume Hamiltonians and prove spectral-threshold stability through the limits directly.",
        "mechanism": "Define gauge-invariant finite-cutoff Hamiltonians, establish uniform form/resolvent convergence and exclude threshold collapse using spectral flow and local observable density.",
        "new": ["finite_cutoff_hamiltonian_family", "uniform_resolvent_flow", "threshold_noncollapse"],
        "p": 0.19, "v": 0.95, "l": 0.88, "c": 0.94,
        "value": "Would reverse the usual Euclidean-to-Hamiltonian order and make the target spectral quantity explicit throughout construction.",
        "learning": "Would identify exactly where threshold stability fails independently of retained-kernel estimates.",
        "question": "Which local compactness and form bounds can prevent a positive finite-cutoff threshold from collapsing in both limits?",
        "corrections": ["Finite-volume gaps collapse despite all available local compactness bounds.", "The Hamiltonian family cannot be shown equivalent to pure Yang--Mills."],
        "sources": [
            (DIRECT_CHALLENGER_ID, "reprioritize", "The claimed transfer operator, OS Hamiltonian, and positive spectral gap directly collide with this route and demand immediate proof-obligation comparison."),
            ("clay-ym-current", "demote", "Official open status forbids treating the challenger or finite-cutoff gaps as the target theorem."),
            ("chatterjee-2401.10507-v4", "split", "Keep the massive Gaussian Yang-Mills-Higgs limit outside pure-gauge Hamiltonian threshold stability."),
        ],
        "priority": "immediate_hamiltonian_claim_collision_audit",
        "revisions": [
            "Audit the challenger's transfer-operator uniformity, OS reconstruction, vacuum sector, and continuum spectral-gap implication line by line.",
            "Retain a direct Hamiltonian programme only if it adds a distinct noncircular threshold-noncollapse route.",
        ],
    },
    {
        "id": "YM21-R09",
        "title": "Observable-first modular reconstruction",
        "corner": "reflexive_inversion",
        "intuition": "The missing object may be a completeness principle for physically accessible observables; local dynamics should be reconstructed from that principle rather than used to prove it later.",
        "mechanism": "Postulate a testable modular-inclusion or quantum-information completeness condition on gauge-invariant subalgebras and derive both recovery across scales and spectral observability.",
        "new": ["observable_completeness_axiom", "modular_inclusion", "scale_recovery_channel"],
        "p": 0.21, "v": 0.93, "l": 0.89, "c": 0.86,
        "value": "Would unify the bundle's separate recovery and dense-core blockers at an observable-algebra level.",
        "learning": "Would decide whether observable completeness has independent content or merely restates the gap.",
        "question": "Can an independently motivated completeness/recovery axiom force every nonvacuum temporal mode to be visible?",
        "corrections": ["The axiom is equivalent to spectral coercivity.", "A hidden-mode countermodel satisfies the proposed recovery conditions."],
        "sources": [
            ("arxiv-1906.00999", "reframe", "Use functorial linear Yang-Mills observable algebras as categorical genealogy, with the interacting/nonlinear boundary explicit."),
            ("arxiv-1410.0664", "reframe", "Use approximate Markov recovery only after constructing the relevant gauge-invariant algebra/state factorization."),
            (DIRECT_CHALLENGER_ID, "reprioritize", "Ask whether the challenger's OS reconstruction establishes the observable completeness this route seeks or silently assumes it."),
        ],
        "priority": "high_priority_observable_reconstruction_audit",
        "revisions": [
            "Define an interacting gauge-invariant observable algebra and independent completeness/recovery criterion.",
            "Prove that recovery controls all nonvacuum temporal modes rather than only a finite-system information distance.",
        ],
    },
    {
        "id": "YM21-R10",
        "title": "Incumbent normalized-kernel control",
        "corner": "conservative_control",
        "intuition": "The most conservative next move is still to prove the named normalized nonlinear SU(2) retained-kernel and partition-ratio inequalities.",
        "mechanism": "Mature the existing retained-state, weighted-defect, and conditional-partition programme with its current hard gates unchanged.",
        "new": ["normalized_retained_kernel", "weighted_defect_ceiling", "conditional_partition_ratio"],
        "p": 0.36, "v": 0.75, "l": 0.66, "c": 0.72,
        "value": "Provides a calibrated control for whether external rivals improve conceptual reach or only vocabulary.",
        "learning": "Establishes the opportunity cost and concrete progress of staying inside the incumbent programme.",
        "question": "Can the first shared nonlinear kernel inequality be closed uniformly without adding a new ontology?",
        "corrections": ["The normalized inequality fails on an admissible history.", "Uniform constants collapse with volume or cutoff."],
        "sources": [
            (DIRECT_CHALLENGER_ID, "reprioritize", "Audit the direct overlap between the challenger's reflection-positive multiscale claims and the incumbent retained-kernel/RG programme before allocating further proof effort."),
            ("clay-ym-current", "demote", "Keep all incumbent and challenger claims below solved-target status."),
            ("mondal-jhep-2023-191", "reframe", "Compare geometric framing before claiming novelty."),
            ("chatterjee-2401.10507-v4", "split", "Keep Higgs scaling results outside the pure-gauge proof chain."),
            ("arxiv-2506.00284-withdrawn", "retire", "Exclude the withdrawn proof claim from support."),
            ("arxiv-2509.19176", "split", "Keep abelian Higgs correlation decay as comparator only."),
        ],
        "priority": "control_requires_direct_claim_collision_audit",
        "revisions": [
            "Build a theorem-level overlap matrix between the incumbent kernel/RG gates and all six June 2026 claims.",
            "Continue the incumbent programme only where its obligations remain distinct, independently motivated, and decision-relevant after the audit.",
        ],
        "control": True,
    },
)


def build_rival_portfolio(literature: dict[str, Any]) -> dict[str, Any]:
    """Build aggressive candidate rivals; externality is evaluated separately."""

    literature_by_id = {row["source_id"]: row for row in literature["sources"]}
    literature_ids = set(literature_by_id)
    literature_digest = sha256_bytes(canonical_bytes(literature))
    basis_digest = sha256_bytes(
        canonical_bytes(
            {
                "target_id": TARGET_ID,
                "literature_digest": literature_digest,
                "incumbent": rel(NORMALIZED_ROOT / "hypothesis_portfolio.json"),
            }
        )
    )
    hypotheses: list[dict[str, Any]] = []
    branches: list[dict[str, Any]] = []
    for index, seed in enumerate(RIVAL_SEEDS, start=1):
        source_ids = [row[0] for row in seed["sources"]]
        if not set(source_ids).issubset(literature_ids):
            raise IntegrationError(f"rival seed has unknown literature source: {seed['id']}")
        is_control = bool(seed.get("control"))
        is_wildcard = bool(seed.get("wildcard"))
        branch_id = f"ym21-rival-branch-{index:02d}"
        hypothesis = {
            "hypothesis_id": seed["id"],
            "title": seed["title"],
            "corner_family": seed["corner"],
            "portfolio_role": "conservative_control" if is_control else "structurally_external_rival",
            "pre_targeted_repair_intuition": {
                "text": seed["intuition"],
                "origin": "user-directed aggressive intuitive hypothesis pass",
                "captured_at": PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT,
                "capture_basis": (
                    "Timestamp of the first durable rival-portfolio materialization; "
                    "the exact earlier in-memory drafting time is unknown."
                ),
                "preserved_verbatim_before_source_mapping": True,
                "full_frontier_search_precedence": "unknown",
                "temporal_boundary": (
                    "The text is preserved verbatim from the first durable portfolio and predates the "
                    f"{PROVIDER_REBASE_RECORDED_AT} targeted provider-backed repair. It is not a pre-search "
                    "claim: the bounded web pass had already begun, precedence relative to every frontier-search "
                    "input is unknown, and this does not record when the idea first occurred."
                ),
            },
            "mechanism": seed["mechanism"],
            "structural_externality": {
                "external_to_incumbent": not is_control,
                "generator_claim_status": "candidate_only_pending_independent_overlap_evaluation",
                "abandons_incumbent_primitives": (
                    ["retained_boundary_kernel", "bad_block_field", "relational_rigidity_basin", "block_RG_controller"]
                    if not is_control
                    else []
                ),
                "new_primitives": seed["new"],
            },
            "target_relevance": {
                "essential_commitments_preserved": ["pure four-dimensional Yang--Mills", "gauge-invariant observables", "physical spectral gap", "continuum identity"],
                "relevance_gate": "passed_as_incubating_theory_seed",
            },
            "risk_reward": {
                "probability_of_truth": seed["p"],
                "value_if_right": seed["v"],
                "learning_value_if_false": seed["l"],
                "maturation_cost": seed["c"],
            },
            "value_if_right": seed["value"],
            "learning_value_if_false": seed["learning"],
            "maturation_question": seed["question"],
            "correction_conditions": seed["corrections"],
            "literature_rebase": {
                "mapping_phase": "targeted_repair_after_bounded_search",
                "mapped_at": literature["retrieved_at"],
                "snapshot_digest": literature_digest,
                "source_ids": source_ids,
                "causal_effects": [
                    {
                        "source_id": source_id,
                        "effect_type": effect_type,
                        "effect": effect,
                        "source_domain": literature_by_id[source_id]["domain"],
                        "transfer_boundary": literature_by_id[source_id]["transfer_boundary"],
                        "claim_status": literature_by_id[source_id]["claim_status"],
                    }
                    for source_id, effect_type, effect in seed["sources"]
                ],
                "priority_effect": {
                    "tier": seed["priority"],
                    "changed_by_source_ids": source_ids,
                    "rationale": (
                        "The bounded search changes reading and maturation order, not truth probability; "
                        "the unverified challenger can require a collision audit but cannot select a theory."
                    ),
                },
                "required_revisions": list(seed["revisions"]),
                "post_targeted_repair_state": (
                    "control_collision_audit_required"
                    if is_control
                    else "incubating_rebased_seed_collision_audit_required"
                    if DIRECT_CHALLENGER_ID in source_ids
                    else "incubating_rebased_seed"
                ),
                "novelty_claim": "unassessed",
                "authority_boundary": (
                    "Provider retrieval and causal mapping can reprioritize theory work only; they do not "
                    "verify source claims, establish novelty, promote truth, or solve the target."
                ),
            },
            "selection_status": "control" if is_control else "protected_wildcard" if is_wildcard else "parallel_seed",
            "parallel_seed": {
                "branch_id": branch_id,
                "wave": 1 + ((index - 1) // 4),
                "frozen_input_digest": basis_digest,
                "artifact_namespace": f"agentic/reports/ym_representational_dynamics_integration/{VERSION}/parallel/{branch_id}",
                "expected_output": "matured theory packet with mechanism, target bridge, source rebase, falsifiers, obligations, and explicit plateau",
            },
            "non_claim_boundary": "Intuitive theory seed only; not a novelty, correctness, continuum, OS, or mass-gap claim.",
        }
        hypotheses.append(hypothesis)
        branches.append(
            {
                "branch_id": branch_id,
                "hypothesis_id": seed["id"],
                "wave": hypothesis["parallel_seed"]["wave"],
                "frozen_input_digest": basis_digest,
                "immutable_seed": True,
                "sibling_reads": "forbidden_until_reduce",
                "allowed_operators": ["frontier-literature-assimilator", "reflective-theory-synthesizer", "high-risk-hypothesis-forger"],
                "optional_support": ["dynamic-symbolic-simulation-experimenter"],
                "budget": {"wall_seconds": 900, "cost_units": 10.0, "storage_bytes": 5_000_000},
                "stop_conditions": ["correction condition met", "target relevance lost", "honest theoretical plateau", "budget exhausted"],
            }
        )
    portfolio: dict[str, Any] = {
        "schema_version": 1,
        "portfolio_id": "ym21-aggressive-structurally-external-rivals",
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "incumbent_portfolio_ref": rel(NORMALIZED_ROOT / "hypothesis_portfolio.json"),
        "literature_snapshot": {
            "snapshot_kind": literature["snapshot_kind"],
            "provider_backed": literature["provider_backed"],
            "live_recency_claim": literature["live_recency_claim"],
            "exhaustive_coverage_claim": literature["exhaustive_coverage_claim"],
            "peer_validation_claim": literature["peer_validation_claim"],
            "retrieved_at": literature["retrieved_at"],
            "snapshot_digest": literature_digest,
            "coverage_cutoff": literature["coverage_cutoff"],
            "coverage_limits": list(literature["coverage_limits"]),
        },
        "generation_charter": {
            "generator_identity": RIVAL_GENERATOR_IDENTITY,
            "theory_first": True,
            "structurally_external_minimum": 8,
            "wildcard_minimum": 2,
            "control_minimum": 1,
            "experiments_role": "secondary_support",
            "selection_rule": "relevance-constrained plural portfolio; no scalar truth/reward collapse",
        },
        "hypotheses": hypotheses,
        "protected_wildcard_ids": [seed["id"] for seed in RIVAL_SEEDS if seed.get("wildcard")],
        "conservative_control_ids": [seed["id"] for seed in RIVAL_SEEDS if seed.get("control")],
        "parallel_maturation_plan": {
            "max_workers": 4,
            "isolation": "immutable branch seed, branch-local receipts, no sibling reads before reducer",
            "frozen_inputs": {"basis_digest": basis_digest, "literature_snapshot_digest": literature_digest},
            "branches": branches,
            "merge_policy": {
                "reducer_only": True,
                "preserve_conflicts": True,
                "preserve_genealogy": True,
                "automatic_truth_selection": False,
                "retain_all_valid_wildcards": True,
            },
            "partial_success_policy": "preserve_valid_siblings",
        },
        "explicit_unknowns": [
            "The durable intuitions predate the targeted repair, but their precedence relative to all prior frontier-search exposure is unknown; they are not blind pre-search artifacts.",
            "Novelty is unassessed beyond the bounded, non-exhaustive provider-backed capture.",
            "The six claims in arXiv:2606.19362 are unverified challengers and have not been independently audited here.",
            "The external browser capture is not an executable discovery-operator receipt and cannot by itself open an active-investment or theorem-promotion gate.",
            "No seed has been matured into a theorem programme or validated for correctness.",
            "Several external programmes may fail to construct pure Yang--Mills or link their native spectrum to the Clay target.",
        ],
    }
    portfolio["content_digest"] = sha256_bytes(canonical_bytes(portfolio))
    return portfolio


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise IntegrationError(f"expected a JSON object: {rel(path)}")
    return payload


def load_direct_claim_mapping_oracle() -> dict[str, Any]:
    """Load and validate the independently authored claim-effects oracle."""

    oracle = _load_json_object(DIRECT_CLAIM_MAPPING_EXPECTATIONS)
    boundary = oracle.get("authorship_boundary", {})
    if (
        oracle.get("schema_version") != 1
        or oracle.get("target_id") != TARGET_ID
        or oracle.get("source_id") != DIRECT_CHALLENGER_ID
        or boundary.get("generator_identity") != RIVAL_GENERATOR_IDENTITY
        or boundary.get("oracle_author_identity") == RIVAL_GENERATOR_IDENTITY
        or boundary.get("independent_from_generator_tables") is not True
        or boundary.get("truth_authority") != "none"
    ):
        raise IntegrationError("direct-claim mapping oracle lacks an independent, non-truth authority boundary")
    rows = oracle.get("claim_mappings")
    if not isinstance(rows, list) or len(rows) != 6:
        raise IntegrationError("direct-claim mapping oracle must contain six claim effects")
    expected_claim_ids = {
        "C2606-transfer-gap",
        "C2606-area-law",
        "C2606-continuum-clustering",
        "C2606-os-hamiltonian",
        "C2606-universality",
        "C2606-weak-strong-bridge",
    }
    if {str(row.get("claim_id")) for row in rows} != expected_claim_ids:
        raise IntegrationError("direct-claim mapping oracle claim set drift")
    target_sets: list[tuple[str, ...]] = []
    rival_ids = {seed["id"] for seed in RIVAL_SEEDS}
    for row in rows:
        affected = row.get("affected_rival_ids")
        if (
            not isinstance(affected, list)
            or not affected
            or len(affected) != len(set(affected))
            or not set(affected).issubset(rival_ids)
            or len(str(row.get("rationale", ""))) < 80
            or len(str(row.get("counterfactual_test", ""))) < 60
        ):
            raise IntegrationError(f"direct-claim mapping oracle row is incomplete: {row.get('claim_id')}")
        target_sets.append(tuple(affected))
    if len(set(target_sets)) != len(target_sets):
        raise IntegrationError("direct challenger claims were broadcast through duplicated rival target sets")
    return oracle


def validate_direct_claim_theory_mappings(
    mappings: Iterable[Mapping[str, Any]], literature: Mapping[str, Any]
) -> None:
    """Fail closed when one challenger claim is broadcast or mapped to the wrong rival."""

    oracle = load_direct_claim_mapping_oracle()
    expected = {row["claim_id"]: row for row in oracle["claim_mappings"]}
    challenger = next(
        row for row in literature["sources"] if row["source_id"] == DIRECT_CHALLENGER_ID
    )
    audits = {row["claim_id"]: row for row in challenger["claim_audit"]}
    actual_rows = [row for row in mappings if row.get("source_id") == DIRECT_CHALLENGER_ID]
    if len(actual_rows) != len(expected):
        raise IntegrationError("direct challenger mapping count differs from the independent oracle")
    seen_claim_ids: set[str] = set()
    for row in actual_rows:
        object_ids = {str(value) for value in row.get("theory_object_ids", [])}
        claim_ids = object_ids & set(expected)
        if len(claim_ids) != 1:
            raise IntegrationError("direct challenger mapping must bind exactly one claim obligation")
        claim_id = next(iter(claim_ids))
        if claim_id in seen_claim_ids:
            raise IntegrationError(f"duplicate direct challenger claim mapping: {claim_id}")
        seen_claim_ids.add(claim_id)
        expected_row = expected[claim_id]
        actual_rivals = sorted(value for value in object_ids if value.startswith("YM21-R"))
        if actual_rivals != sorted(expected_row["affected_rival_ids"]):
            raise IntegrationError(f"claim-specific rival mapping drift: {claim_id}")
        conceptual_change = str(row.get("conceptual_change", ""))
        if (
            expected_row["rationale"] not in conceptual_change
            or expected_row["counterfactual_test"] not in conceptual_change
            or row.get("exact_claim") != audits[claim_id]["author_stated_claim"]
        ):
            raise IntegrationError(f"claim mapping lacks independent rationale/counterfactual: {claim_id}")
    if seen_claim_ids != set(expected):
        raise IntegrationError("direct challenger claim mapping is incomplete")


def _candidate_overlap_basis(portfolio: Mapping[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        (
            {
                "hypothesis_id": row["hypothesis_id"],
                "title": row["title"],
                "mechanism": row["mechanism"],
                "new_primitives": row["structural_externality"]["new_primitives"],
            }
            for row in portfolio["hypotheses"]
        ),
        key=lambda row: row["hypothesis_id"],
    )


def build_incumbent_overlap_evaluation(portfolio: Mapping[str, Any]) -> dict[str, Any]:
    """Bind a typed, independently authored overlap judgment to exact candidate text."""

    oracle = _load_json_object(INCUMBENT_OVERLAP_EXPECTATIONS)
    if (
        oracle.get("schema_version") != 1
        or oracle.get("target_id") != TARGET_ID
        or oracle.get("generator_identity") != RIVAL_GENERATOR_IDENTITY
        or oracle.get("evaluator_identity") == RIVAL_GENERATOR_IDENTITY
        or oracle.get("independence", {}).get("identity_distinct_from_generator") is not True
        or oracle.get("independence", {}).get("generator_externality_flags_treated_as_untrusted_inputs") is not True
        or oracle.get("independence", {}).get("truth_authority") != "none"
    ):
        raise IntegrationError("incumbent-overlap oracle is not independently scoped")
    evaluation = json.loads(json.dumps(oracle))
    evaluation["evaluated_portfolio_ref"] = rel(NORMALIZED_ROOT / "aggressive_rival_portfolio.json")
    evaluation["candidate_set_digest"] = sha256_bytes(canonical_bytes(_candidate_overlap_basis(portfolio)))
    evaluation["evaluated_at"] = "2026-07-21T22:35:00+02:00"
    evaluation["authority_boundary"] = (
        "The evaluator classifies conceptual overlap and externality only. It does not assess theorem truth, "
        "source correctness, target resolution, or novelty beyond the declared comparison basis."
    )
    evaluation["content_digest"] = sha256_bytes(canonical_bytes(evaluation))
    validate_incumbent_overlap_evaluation(evaluation, portfolio)
    return evaluation


def validate_incumbent_overlap_evaluation(
    evaluation: Mapping[str, Any], portfolio: Mapping[str, Any]
) -> None:
    """Validate typed overlap coverage independently of generator externality flags."""

    digest_payload = dict(evaluation)
    observed_digest = digest_payload.pop("content_digest", None)
    if observed_digest != sha256_bytes(canonical_bytes(digest_payload)):
        raise IntegrationError("incumbent-overlap evaluation digest mismatch")
    expected_candidate_digest = sha256_bytes(canonical_bytes(_candidate_overlap_basis(portfolio)))
    if evaluation.get("candidate_set_digest") != expected_candidate_digest:
        raise IntegrationError("incumbent-overlap evaluation is not bound to the candidate text")
    if (
        evaluation.get("generator_identity") != RIVAL_GENERATOR_IDENTITY
        or evaluation.get("evaluator_identity") == RIVAL_GENERATOR_IDENTITY
        or evaluation.get("independence", {}).get("truth_authority") != "none"
    ):
        raise IntegrationError("incumbent-overlap evaluator is not independent from the generator")
    rows = evaluation.get("evaluations")
    if not isinstance(rows, list):
        raise IntegrationError("incumbent-overlap evaluation lacks rows")
    candidate_ids = {row["hypothesis_id"] for row in portfolio["hypotheses"]}
    if {row.get("candidate_id") for row in rows} != candidate_ids:
        raise IntegrationError("incumbent-overlap evaluation does not cover every candidate exactly once")
    if len(rows) != len(candidate_ids):
        raise IntegrationError("incumbent-overlap evaluation duplicates candidates")
    allowed_types = set(evaluation.get("type_vocabulary", []))
    allowed_verdicts = set(evaluation.get("verdict_vocabulary", []))
    for row in rows:
        if (
            not row.get("incumbent_object_ids")
            or not row.get("overlap_types")
            or not set(row["overlap_types"]).issubset(allowed_types)
            or row.get("verdict") not in allowed_verdicts
            or len(str(row.get("rationale", ""))) < 50
            or len(str(row.get("counterfactual_test", ""))) < 30
        ):
            raise IntegrationError(f"typed incumbent-overlap row is incomplete: {row.get('candidate_id')}")
    by_id = {row["candidate_id"]: row for row in rows}
    if by_id["YM21-R10"]["verdict"] != "incumbent_control_identity":
        raise IntegrationError("incumbent control was misclassified as external")
    for candidate_id in ("YM21-R01", "YM21-R02", "YM21-R08", "YM21-R09"):
        if "endpoint_overlap" not in by_id[candidate_id]["overlap_types"]:
            raise IntegrationError(f"known endpoint overlap was omitted: {candidate_id}")


CANONICAL_LANE_SOURCE_IDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "closest_known_work",
        ("clay-ym-current", DIRECT_CHALLENGER_ID, "mondal-jhep-2023-191"),
    ),
    (
        "recent_frontier_preprints",
        (
            DIRECT_CHALLENGER_ID,
            "arxiv-2503.03060",
            "chatterjee-2401.10507-v4",
            "arxiv-2509.19176",
        ),
    ),
    (
        "negative_results_barriers",
        ("arxiv-2506.00284-withdrawn", "clay-ym-current", DIRECT_CHALLENGER_ID),
    ),
    (
        "conceptual_genealogy",
        ("arxiv-1412.5148", "arxiv-1703.00501", "arxiv-1906.00999"),
    ),
    (
        "adjacent_field_mechanisms",
        (
            "arxiv-2201.03487",
            "arxiv-2006.04987",
            "arxiv-1410.0664",
            "chatterjee-2401.10507-v4",
        ),
    ),
    (
        "dissenting_positions",
        (DIRECT_CHALLENGER_ID, "mondal-jhep-2023-191", "clay-ym-current"),
    ),
)


def _canonical_source_type(source: Mapping[str, Any]) -> str:
    """Project rich dated source kinds into the central closed vocabulary."""

    raw = str(source.get("source_type", ""))
    if source.get("source_status") == "withdrawn":
        return "retraction"
    if "preprint" in raw and "journal" not in raw:
        return "preprint"
    if "research" in raw:
        return "primary"
    return "other"


def _canonical_literature_snapshot(
    literature: Mapping[str, Any], *, theory_state_digest: str
) -> dict[str, Any]:
    """Conservatively project the richer manual capture to the central snapshot.

    Central ``live`` authority is deliberately withheld: the browser calls were
    real, but they were not issued by a receipt-producing discovery operator.
    Encoding every lane as ``local_only`` retains decision-relevant source and
    query fields while explicitly omitting provider ranking payloads and richer
    dated metadata that the central closed vocabulary cannot represent.
    """

    sources_by_id = {row["source_id"]: row for row in literature["sources"]}
    query_by_id = {row["query_id"]: row for row in literature["queries"]}
    lanes_by_source: dict[str, list[str]] = {source_id: [] for source_id in sources_by_id}
    lane_receipts: list[dict[str, Any]] = []
    for lane_type, source_ids in CANONICAL_LANE_SOURCE_IDS:
        lane_id = f"ym21-{lane_type.replace('_', '-')}"
        for source_id in source_ids:
            lanes_by_source[source_id].append(lane_id)
        query_ids = sorted(
            {
                query_id
                for source_id in source_ids
                for query_id in sources_by_id[source_id]["query_ids"]
            }
        )
        provider_ids = sorted({sources_by_id[source_id]["provider_id"] for source_id in source_ids})
        indexes = sorted({sources_by_id[source_id]["index"] for source_id in source_ids})
        receipt: dict[str, Any] = {
            "lane_id": lane_id,
            "lane_type": lane_type,
            "queries": [query_by_id[query_id]["text"] for query_id in query_ids],
            "provider": "external-manual-capture:" + "+".join(provider_ids),
            "index": "; ".join(indexes),
            "execution_mode": "local_only",
            "started_at": literature["retrieval_window"]["started_at"],
            "completed_at": literature["retrieval_window"]["completed_at"],
            "status": "completed",
            "result_count": len(source_ids),
            "source_ids": sorted(source_ids),
            "coverage_cutoff": literature["coverage_cutoff"],
            "inclusion_policy": literature["inclusion_policy"],
            "exclusion_policy": (
                "Exclude target-mismatched records and any transfer that erases dimension, matter content, "
                "gauge group, correction status, regulator, or proof-obligation boundaries."
            ),
            "failure": None,
        }
        receipt["content_digest"] = canonical_digest(receipt)
        receipt["validator_receipt_ids"] = [
            stable_identifier("ym21-lane-validator", lane_id, receipt["content_digest"])
        ]
        lane_receipts.append(receipt)

    central_sources: list[dict[str, Any]] = []
    for source_id, source in sources_by_id.items():
        url = str(source["url"])
        arxiv_id = url.rsplit("/", 1)[-1] if "arxiv.org/abs/" in url else None
        claims = [str(item) for item in source.get("reported_claims", [])]
        claims.extend(
            str(item["author_stated_claim"])
            for item in source.get("claim_audit", [])
            if str(item.get("author_stated_claim", "")).strip()
        )
        row: dict[str, Any] = {
            "source_id": source_id,
            "work_identity": f"arxiv:{arxiv_id}" if arxiv_id else f"url:{url}",
            "title": source["title"],
            "authors": list(source["authors"]),
            "publication_date": source["publication_date"],
            "source_version": source["source_version"],
            "source_type": _canonical_source_type(source),
            "url": url,
            "doi": None,
            "arxiv_id": arxiv_id,
            "correction_status": (
                "retracted"
                if source["source_status"] == "withdrawn"
                else "unknown"
                if source["claim_status"] == "unverified_challenger"
                else "none_known"
            ),
            "lane_ids": sorted(set(lanes_by_source[source_id])),
            "decision_relevant": True,
            "claims": sorted(set(claims)),
            "limitations": [
                source["transfer_boundary"],
                "External provider retrieval is not executable operator provenance and cannot validate this claim.",
            ],
        }
        row["content_digest"] = canonical_digest(row)
        central_sources.append(row)
    central_sources.sort(key=lambda row: row["source_id"])

    core: dict[str, Any] = {
        "schema_version": "1.0",
        "snapshot_id": stable_identifier(
            "ym21-literature-snapshot",
            TARGET_ID,
            theory_state_digest,
            literature["retrieved_at"],
            [row["source_id"] for row in central_sources],
        ),
        "target_id": TARGET_ID,
        "claim_scope": (
            "Pure four-dimensional Yang-Mills existence and mass gap, direct 2026 claim collision, "
            "and lane-specific conceptual genealogy"
        ),
        "theory_state_digest": theory_state_digest,
        "search_started_at": literature["retrieval_window"]["started_at"],
        "search_completed_at": literature["retrieval_window"]["completed_at"],
        "coverage_cutoff": literature["coverage_cutoff"],
        "provenance_mode": "local_only",
        "inclusion_policy": literature["inclusion_policy"],
        "exclusion_policy": (
            "Exclude target-mismatched records, withdrawn records as support, and every transfer that "
            "silently changes dimension, matter content, gauge group, or proof status."
        ),
        "lane_receipts": lane_receipts,
        "sources": central_sources,
        "result_count": len(central_sources),
        "coverage_limits": [
            *literature["coverage_limits"],
            "Canonical authority is local_only because no executable literature-search operator receipt produced this external browser capture.",
        ],
        "duplicate_groups": [],
        "claim_conflicts": [
            {
                "conflict_id": "ym21-open-status-vs-2606-claim",
                "source_ids": ["clay-ym-current", DIRECT_CHALLENGER_ID],
                "tension": "An unverified June 2026 paper claims the target while the official acceptance boundary remains open.",
                "resolution": "Keep the paper as an unverified challenger and open six proof obligations; do not promote target status.",
            }
        ],
    }
    core["content_digest"] = canonical_digest(core)
    core["validator_receipts"] = [
        {
            "receipt_id": stable_identifier(
                "ym21-snapshot-validator", core["snapshot_id"], core["content_digest"]
            ),
            "validator_id": "ym21-external-capture-adapter-validator.v1",
            "status": "passed",
            "validated_digest": core["content_digest"],
            "completed_at": literature["retrieved_at"],
            "reason_codes": [
                "schema_and_digest_valid",
                "external_browser_capture_not_operator_receipt",
                "active_investment_must_remain_blocked_local_only",
            ],
        }
    ]
    core["validation_status"] = "validated"
    validate_snapshot(core)
    return core


def build_canonical_literature_interop(
    literature: Mapping[str, Any],
    rival_portfolio: Mapping[str, Any],
    *,
    theory_state_digest: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Emit central-schema artifacts without upgrading manual search authority."""

    theory_digest = theory_state_digest or canonical_digest(
        {
            "target_id": TARGET_ID,
            "source_version": VERSION,
            "basis": "dated YM21 literature-adapter template; bind an active canonical state before use",
        }
    )
    snapshot = _canonical_literature_snapshot(literature, theory_state_digest=theory_digest)
    source_targets: dict[str, set[str]] = {row["source_id"]: set() for row in literature["sources"]}
    for hypothesis in rival_portfolio["hypotheses"]:
        for source_id in hypothesis["literature_rebase"]["source_ids"]:
            source_targets[source_id].add(hypothesis["hypothesis_id"])

    claim_oracle = load_direct_claim_mapping_oracle()
    claim_effects = {
        row["claim_id"]: row for row in claim_oracle["claim_mappings"]
    }
    mappings: list[dict[str, Any]] = []
    for source in literature["sources"]:
        source_id = source["source_id"]
        theory_ids = sorted(source_targets[source_id] or {"YM21-R10"})
        relation = {
            "demote": "contradicts",
            "retire": "contradicts",
            "split": "sharpens",
            "reframe": "reframes",
            "reprioritize": "leaves_open",
            "unchanged": "leaves_open",
        }.get(source["effect_type"], "leaves_open")
        event_type = (
            "justified_no_change" if source["effect_type"] == "unchanged" else source["effect_type"]
        )
        if source_id == DIRECT_CHALLENGER_ID:
            for audit in source["claim_audit"]:
                effect = claim_effects[audit["claim_id"]]
                claim_theory_ids = sorted(
                    {*effect["affected_rival_ids"], audit["claim_id"]}
                )
                mappings.append(
                    {
                        "mapping_id": stable_identifier(
                            "ym21-source-map", source_id, audit["claim_id"], claim_theory_ids
                        ),
                        "source_id": source_id,
                        "theory_object_ids": claim_theory_ids,
                        "object_kinds": ["hypothesis", "proof_obligation", "schedule"],
                        "relation": "leaves_open",
                        "exact_claim": audit["author_stated_claim"],
                        "source_limitation": source["transfer_boundary"],
                        "conceptual_change": (
                            f"Create an unverified-challenger collision obligation: {audit['required_obligation']} "
                            f"Claim-specific rationale: {effect['rationale']} "
                            f"Counterfactual mapping test: {effect['counterfactual_test']}"
                        ),
                        "event_type": "reprioritize",
                        "coverage_limits": list(literature["coverage_limits"]),
                        "confidence": "low",
                    }
                )
            continue
        mappings.append(
            {
                "mapping_id": stable_identifier("ym21-source-map", source_id, theory_ids, event_type),
                "source_id": source_id,
                "theory_object_ids": theory_ids,
                "object_kinds": ["genealogy", "hypothesis", "proof_obligation"],
                "relation": relation,
                "exact_claim": source["reported_claims"][0],
                "source_limitation": source["transfer_boundary"],
                "conceptual_change": source["source_to_theory_delta"],
                "event_type": event_type,
                "coverage_limits": list(literature["coverage_limits"]),
                "confidence": "high" if source_id == "clay-ym-current" else "medium",
            }
        )
    validate_direct_claim_theory_mappings(mappings, literature)

    hypotheses = []
    for hypothesis in rival_portfolio["hypotheses"]:
        rebase = hypothesis["literature_rebase"]
        hypotheses.append(
            {
                "hypothesis_id": hypothesis["hypothesis_id"],
                "genealogy": [hypothesis["hypothesis_id"], hypothesis["corner_family"]],
                "literature_relation": (
                    "partly_anticipated"
                    if DIRECT_CHALLENGER_ID in rebase["source_ids"]
                    else "cross_field_bridge"
                ),
                "source_ids": rebase["source_ids"],
                "required_revision": " ".join(rebase["required_revisions"]),
                "routing_effect": (
                    "targeted_reading"
                    if DIRECT_CHALLENGER_ID in rebase["source_ids"]
                    else "sharpen"
                ),
            }
        )
    assimilation = assimilate_literature(
        snapshot,
        theory_state_digest=theory_digest,
        theory_mappings=mappings,
        hypotheses=hypotheses,
        candidate_snapshot_ids=[snapshot["snapshot_id"]],
    )
    validate_assimilation(assimilation, snapshot=snapshot)
    return snapshot, assimilation


def registered_runtime_binding_if_present() -> dict[str, Any] | None:
    """Return the validated active-current runtime upgrade, if it has completed."""

    acceptance_path = REGISTERED_RUNTIME_ROOT / "acceptance_report.json"
    result_path = REGISTERED_RUNTIME_ROOT / "canonical_cycle_result.json"
    receipts_path = REGISTERED_RUNTIME_ROOT / "operator_receipts.json"
    roles_path = REGISTERED_RUNTIME_ROOT / "artifact_roles.json"
    snapshot_path = (
        REGISTERED_RUNTIME_ROOT
        / "workspace/artifacts/00-frozen-live-literature-snapshot.json"
    )
    required = (
        acceptance_path,
        result_path,
        receipts_path,
        roles_path,
        snapshot_path,
    )
    if not all(path.exists() for path in required):
        return None
    acceptance = _load_json_object(acceptance_path)
    result = _load_json_object(result_path)
    receipts_packet = _load_json_object(receipts_path)
    roles = _load_json_object(roles_path)
    snapshot = _load_json_object(snapshot_path)
    validate_snapshot(snapshot)
    receipts = receipts_packet.get("receipts")
    if not isinstance(receipts, list):
        raise IntegrationError("registered YM runtime lacks operator receipts")
    operator_ids = {row["operator"]["operator_id"] for row in receipts}
    expected_operators = {
        "frontier-literature-assimilator",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "reflective-conceptual-discovery",
        "dynamic-symbolic-simulation-experimenter",
        "reflective-theory-synthesizer",
    }
    if (
        acceptance.get("status") != "passed"
        or not all(acceptance.get("checks", {}).values())
        or len(receipts) != 6
        or operator_ids != expected_operators
        or any(row.get("status") != "succeeded" for row in receipts)
        or snapshot.get("provenance_mode") != "live"
        or result.get("literature_basis", {}).get("mode") != "active_current"
        or result.get("committed_state_version") != 1
    ):
        raise IntegrationError("registered YM runtime did not satisfy active-current acceptance")
    assimilation_relative = roles.get("literature_assimilation")
    if not isinstance(assimilation_relative, str):
        raise IntegrationError("registered YM runtime lacks an assimilation role binding")
    assimilation_path = REGISTERED_RUNTIME_ROOT / "workspace" / assimilation_relative
    assimilation = _load_json_object(assimilation_path)
    validate_assimilation(assimilation, snapshot=snapshot)
    literature_receipt = next(
        row
        for row in receipts
        if row["operator"]["operator_id"] == "frontier-literature-assimilator"
    )
    return {
        "schema_version": 1,
        "binding_id": "ym21-registered-active-current-runtime-20260721",
        "status": "active_current",
        "target_id": TARGET_ID,
        "run_id": "ym21-canonical-parent-20260721",
        "snapshot": {
            "path": rel(snapshot_path),
            "snapshot_id": snapshot["snapshot_id"],
            "content_digest": snapshot["content_digest"],
            "provenance_mode": "live",
            "lane_count": len(snapshot["lane_receipts"]),
        },
        "assimilation": {
            "path": rel(assimilation_path),
            "packet_id": assimilation["packet_id"],
            "content_digest": assimilation["content_digest"],
            "hypothesis_rebase_status": assimilation["hypothesis_rebase_status"],
            "active_investment_gate": assimilation["resolution"]["active_investment_gate"],
            "operator_receipt_id": literature_receipt["receipt_id"],
        },
        "canonical_cycle": {
            "result_path": rel(result_path),
            "commit_id": result["commit_id"],
            "committed_state_version": result["committed_state_version"],
            "manifest_digest": result["manifest_digest"],
            "feedback_edge_count": len(result["feedback_edges"]),
        },
        "acceptance": {
            "path": rel(acceptance_path),
            "acceptance_id": acceptance["acceptance_id"],
            "status": acceptance["status"],
            "content_sha256": sha256_file(acceptance_path),
        },
        "operator_receipts": {
            "path": rel(receipts_path),
            "count": len(receipts),
            "operator_ids": sorted(operator_ids),
        },
        "projection_relationship": (
            "Supersedes the local_only adapter as the active cycle literature authority; the older "
            "conservative projection remains a provenance-preserving historical artifact, not the active status."
        ),
        "authority_boundary": (
            "Active-current status proves registered search-response replay, assimilation, and canonical "
            "commit reachability only; it does not validate source claims, novelty, or the Yang-Mills target."
        ),
    }


def bind_registered_canonical_runtime() -> dict[str, Any]:
    """Bind the accepted live runtime into normalized rebase/registry/report views."""

    binding = registered_runtime_binding_if_present()
    if binding is None:
        raise IntegrationError("registered YM canonical runtime is incomplete")
    write_json(REGISTERED_RUNTIME_BINDING, binding)

    rival_path = NORMALIZED_ROOT / "aggressive_rival_portfolio.json"
    rival = _load_json_object(rival_path)
    rival["canonical_literature_interop"]["registered_runtime_upgrade"] = binding
    rival.pop("content_digest", None)
    rival["content_digest"] = sha256_bytes(canonical_bytes(rival))
    write_json(rival_path, rival)

    rebase_path = NORMALIZED_ROOT / "literature_rebase.json"
    rebase = _load_json_object(rebase_path)
    rebase["active_canonical_literature_status"] = "active_current"
    rebase["registered_runtime_upgrade"] = binding
    rebase["authority_boundary"] = (
        "The historical closed-vocabulary adapter remains explicitly local_only, while the separately "
        "receipt-backed registered runtime is now the active_current canonical authority for this cycle. "
        "Neither path validates source claims or authorizes truth promotion."
    )
    write_json(rebase_path, rebase)

    registry = _load_json_object(YM_REGISTRY)
    registry["canonical_literature_interop"]["registered_runtime_upgrade"] = binding
    registry["pre_cycle_hook"]["last_completed_runtime_status"] = "active_current"
    registry["pre_cycle_hook"]["last_completed_runtime_binding"] = rel(
        REGISTERED_RUNTIME_BINDING
    )
    write_json(YM_REGISTRY, registry)

    report_path = REPORT_ROOT / "integration_report.json"
    report = _load_json_object(report_path)
    report["registered_canonical_runtime"] = binding
    report["canonical_literature_interop"]["active_runtime_status"] = "active_current"
    write_json(report_path, report)

    assessment_paths = (
        NORMALIZED_ROOT / "conceptual_assessment.md",
        REPORT_ROOT / "conceptual_assessment.md",
    )
    section = f"""

## Registered active-current runtime upgrade

The previously described `local_only` packet remains the honest conservative
projection of the manual bounded capture.  It is no longer the active runtime
status for this completed cycle.  The six registered operators executed and
committed under `{binding['run_id']}`; the live snapshot, assimilator receipt,
six feedback edges, canonical commit, and acceptance checks are bound in
`{rel(REGISTERED_RUNTIME_BINDING)}`.  This upgrade authorizes active theory
investment for the recorded cycle only.  It does not validate any source claim,
novelty assertion, continuum construction, or mass-gap proof.
"""
    for path in assessment_paths:
        text = path.read_text(encoding="utf-8")
        if "## Registered active-current runtime upgrade" not in text:
            path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return binding


def normalize_evidence(
    index: dict[str, dict[str, Any]],
    literature: dict[str, Any],
    *,
    theory_state_digest: str | None = None,
) -> None:
    """Create target-bound evidence records without promoting upstream prose to fact."""

    stage52 = source_reference("52_conceptual_restrategy/HYPOTHESIS_STATUS_LEDGER.md", index)
    roadmap = source_reference("52_conceptual_restrategy/BEST_REWARD_ROADMAP.md", index)
    stage78 = source_reference("78_hypothesis_run_audit/AUDIT_REPORT.md", index)
    stage79 = source_reference("79_hypothesis_execution_synthesis/EXECUTION_SYNTHESIS.md", index)
    portfolio_source = source_reference("HYPOTHESIS_STREAM_PORTFOLIO.md", index)

    portfolio = {
        "schema_version": 1,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "epistemic_status": "source-bound restricted/conditional hypothesis portfolio; not independently promoted",
        "source_claim_ceiling": "C2 for finite/restricted theorems; C3 only for explicit conditional implications",
        "shared_first_physical_blocker": (
            "Construct a normalized reflection-positive nonlinear SU(2) retained-boundary conditional kernel "
            "from the actual lattice measure, uniformly over admissible positive-mass histories, finite volume, and cutoff."
        ),
        "hypotheses": [
            {
                "hypothesis_id": hypothesis_id,
                "title": title,
                "strongest_source_result": strongest,
                "first_open_implication": first_open,
                "status": "incumbent_program_branch",
                "claim_level": "C2_restricted_or_C3_conditional",
                "sources": [portfolio_source, stage79],
            }
            for hypothesis_id, title, strongest, first_open in HYPOTHESES
        ],
        "source_genealogy": {"stage_52": [stage52, roadmap], "independent_audit": [stage78], "execution_synthesis": [stage79]},
        "non_claims": [
            "No physical normalized nonlinear SU(2) retained kernel is constructed.",
            "No boundary-, volume-, cutoff-, or retained-history-uniform physical estimate is proved.",
            "No continuum existence, OS reconstruction, theory identity, or Hamiltonian mass gap follows.",
        ],
    }
    write_json(NORMALIZED_ROOT / "hypothesis_portfolio.json", portfolio)

    evidence = {
        "schema_version": 1,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "records": [
            {
                "evidence_id": "YM21-E52",
                "kind": "hypothesis_generation_genealogy",
                "status": "imported_source_claim",
                "claim": "Stage 52 records a ten-stream conceptual restrategy and reward roadmap.",
                "sources": [stage52, roadmap],
                "effect": "Seed target-specific branches while preserving their incumbent-program ancestry.",
            },
            {
                "evidence_id": "YM21-E78",
                "kind": "independent_source_audit",
                "status": "imported_source_claim_requiring_local_replay",
                "claim": "Stage 78 audits Stages 68--75 at restricted levels and preserves exactness qualifications.",
                "sources": [stage78],
                "effect": "Adopt the downgrade boundaries; local replay evidence controls executable status.",
            },
            {
                "evidence_id": "YM21-E79",
                "kind": "cross_stream_synthesis",
                "status": "imported_source_claim_requiring_local_replay",
                "claim": "Stage 79 reports a 194-test H1--H10 execution synthesis and a shared physical blocker.",
                "sources": [stage79],
                "effect": "Retain the cross-stream map but do not import its test total as local evidence.",
            },
        ],
        "replay_authority": rel(REPORT_ROOT / "replay_report.json"),
        "literature_basis_digest": sha256_bytes(canonical_bytes(literature)),
    }
    write_json(NORMALIZED_ROOT / "evidence_ledger.json", evidence)

    rival_portfolio = build_rival_portfolio(literature)
    overlap_evaluation = build_incumbent_overlap_evaluation(rival_portfolio)
    write_json(INCUMBENT_OVERLAP_EVALUATION, overlap_evaluation)
    rival_portfolio["incumbent_overlap_evaluation"] = {
        "path": rel(INCUMBENT_OVERLAP_EVALUATION),
        "evaluation_id": overlap_evaluation["evaluation_id"],
        "generator_identity": overlap_evaluation["generator_identity"],
        "evaluator_identity": overlap_evaluation["evaluator_identity"],
        "candidate_set_digest": overlap_evaluation["candidate_set_digest"],
        "content_digest": overlap_evaluation["content_digest"],
        "binding_status": "independent_post_generation_overlap_evaluation",
        "truth_authority": "none",
    }
    canonical_snapshot, canonical_assimilation = build_canonical_literature_interop(
        literature,
        rival_portfolio,
        theory_state_digest=theory_state_digest,
    )
    write_json(CANONICAL_LITERATURE_SNAPSHOT, canonical_snapshot)
    write_json(CANONICAL_LITERATURE_ASSIMILATION, canonical_assimilation)
    canonical_interop = {
        "snapshot_path": rel(CANONICAL_LITERATURE_SNAPSHOT),
        "snapshot_id": canonical_snapshot["snapshot_id"],
        "snapshot_content_digest": canonical_snapshot["content_digest"],
        "assimilation_path": rel(CANONICAL_LITERATURE_ASSIMILATION),
        "assimilation_packet_id": canonical_assimilation["packet_id"],
        "assimilation_content_digest": canonical_assimilation["content_digest"],
        "theory_state_digest": canonical_snapshot["theory_state_digest"],
        "provenance_mode": canonical_snapshot["provenance_mode"],
        "hypothesis_rebase_status": canonical_assimilation["hypothesis_rebase_status"],
        "active_investment_gate": canonical_assimilation["resolution"]["active_investment_gate"],
        "projection_mode": "conservative_closed_vocabulary_projection",
        "projection_omissions": [
            "provider ranking payloads and result-page HTML not exposed by the provider",
            "rich source-domain and transfer-boundary fields represented only as limitations",
            "manual retrieval-session structure not expressible as executable lane receipts",
        ],
        "authority_boundary": (
            "Conservative central-schema projection only; no lossless-equivalence claim is made. External "
            "browser retrieval was real but not produced by an executable operator receipt, so canonical "
            "authority remains local_only and active investment, novelty, theorem promotion, and truth "
            "selection remain blocked."
        ),
    }
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None:
        canonical_interop["registered_runtime_upgrade"] = runtime_binding
    rival_portfolio["canonical_literature_interop"] = canonical_interop
    rival_portfolio.pop("content_digest", None)
    rival_portfolio["content_digest"] = sha256_bytes(canonical_bytes(rival_portfolio))
    write_json(NORMALIZED_ROOT / "aggressive_rival_portfolio.json", rival_portfolio)

    rebase = {
        "schema_version": 2,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "search_provenance": {
            "snapshot_kind": literature["snapshot_kind"],
            "provider_backed": literature["provider_backed"],
            "live_recency_claim": literature["live_recency_claim"],
            "exhaustive_coverage_claim": literature["exhaustive_coverage_claim"],
            "peer_validation_claim": literature["peer_validation_claim"],
            "searched_at": literature["searched_at"],
            "retrieved_at": literature["retrieved_at"],
            "retrieval_window": literature["retrieval_window"],
            "retrieval_sessions": literature["retrieval_sessions"],
            "coverage_cutoff": literature["coverage_cutoff"],
            "providers": literature["providers"],
            "queries": literature["queries"],
            "inclusion_policy": literature["inclusion_policy"],
            "coverage_limits": literature["coverage_limits"],
            "epistemic_boundary": literature["epistemic_boundary"],
            "snapshot_digest": sha256_bytes(canonical_bytes(literature)),
            "broad_frontier_capture": {
                "path": rel(BROAD_FRONTIER_CAPTURE),
                "capture_id": _load_json_object(BROAD_FRONTIER_CAPTURE)["capture_id"],
                "content_digest": sha256_file(BROAD_FRONTIER_CAPTURE),
                "role": "subsequent broad non-ID-seeded surveillance with raw dispositions",
                "chronology_effect": "does not retroactively make the earlier intuition capture pre-search",
            },
        },
        "sources": literature["sources"],
        "canonical_literature_interop": canonical_interop,
        "rival_lane_rebase": [
            {
                "hypothesis_id": hypothesis["hypothesis_id"],
                "corner_family": hypothesis["corner_family"],
                "pre_targeted_repair_captured_at": hypothesis["pre_targeted_repair_intuition"]["captured_at"],
                "targeted_repair_mapped_at": hypothesis["literature_rebase"]["mapped_at"],
                "full_frontier_search_precedence": hypothesis["pre_targeted_repair_intuition"]["full_frontier_search_precedence"],
                "source_ids": hypothesis["literature_rebase"]["source_ids"],
                "causal_effects": hypothesis["literature_rebase"]["causal_effects"],
                "priority_effect": hypothesis["literature_rebase"]["priority_effect"],
                "required_revisions": hypothesis["literature_rebase"]["required_revisions"],
            }
            for hypothesis in rival_portfolio["hypotheses"]
        ],
        "portfolio_effect": {
            "promotion": "none",
            "direct_challenger": {
                "source_id": DIRECT_CHALLENGER_ID,
                "status": "unverified_challenger",
                "claim_obligation_count": len(
                    next(
                        source["claim_audit"]
                        for source in literature["sources"]
                        if source["source_id"] == DIRECT_CHALLENGER_ID
                    )
                ),
                "effect": "reprioritize collision audits without claim promotion or truth selection",
            },
            "stale_or_corrected_branches": [
                "Any branch claiming the Clay target is solved",
                "Any branch ignoring the June 2026 direct claim collision",
                "Any novelty claim lacking lane-specific primary-source comparison",
            ],
            "retained_value": [
                "finite exact countermodels and representation diagnostics",
                "conditional-kernel normalization and observability obligations",
                "negative knowledge about defect-only spectral inference",
            ],
            "current_frontier": "pure four-dimensional Yang--Mills existence and mass gap remains open",
        },
        "required_before_every_target_cycle": True,
        "authority_boundary": (
            "The dated provider capture causally rebases theory priorities, but only a matching "
            "receipt-backed central search can upgrade canonical provenance from local_only."
        ),
    }
    if runtime_binding is not None:
        rebase["active_canonical_literature_status"] = "active_current"
        rebase["registered_runtime_upgrade"] = runtime_binding
        rebase["authority_boundary"] = (
            "The historical closed-vocabulary adapter remains explicitly local_only, while the separately "
            "receipt-backed registered runtime is active_current for the committed cycle. Neither path "
            "validates source claims or authorizes truth promotion."
        )
    write_json(NORMALIZED_ROOT / "literature_rebase.json", rebase)

    publication_map = {
        "schema_version": 1,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "policy": "external_only_until_separately_scoped_and_current-literature-grounded",
        "skills": [
            {
                "skill": skill,
                "source": source_reference(
                    f"11_vscode_codex_skill_bundle/.agents/skills/{skill}/SKILL.md", index
                ),
                "local_activation": False,
                "reason": "publication composition is downstream of discovery and cannot certify novelty or truth",
            }
            for skill in PUBLICATION_SKILLS
        ],
    }
    write_json(NORMALIZED_ROOT / "publication_capability_map.json", publication_map)

    assessment = f"""# Conceptual assessment of the 2026-07-21 YM bundle

This assessment is an Abducer integration judgment, not an upstream claim.  It
is bound to `{stage52['source_path']}`, `{stage78['source_path']}`, and
`{stage79['source_path']}` and to literature snapshot
`{sha256_bytes(canonical_bytes(literature))}`.

## What the bundle genuinely adds

The bundle is unusually disciplined about finite claim levels, hostile
counterexamples, normalization, exactness, and the still-open continuum/OS
chain.  Its ten streams preserve useful negative knowledge and separate
measure construction, representational transport, and spectral interpretation.
That is a major improvement in articulation and falsifiability.

## The conceptual limitation

The portfolio is predominantly **incumbent elaboration, not plural conceptual
discovery**.  H1--H10 are operationally independent, but most inhabit the same
retained-kernel, relational-rigidity, block-RG, defect-control programme.  They
vary mechanisms inside that ontology more than they rival the ontology itself.
Consequently, their number must not be used as evidence of deep conceptual
plurality, and their shared blocker must not become Abducer's parent controller.

The deepest risk is a self-sealing programme: every failure can be translated
into another missing kernel estimate while the possibility that retained-state,
defect, or rigidity language is the wrong explanatory grain remains under-tested.
The bundle should therefore enter as target evidence and branch seeds under the
reflective conceptual parent loop, never as the parent loop itself.

## Dated provider-backed literature rebase

The first durable copies of the aggressive intuition strings are timestamped
`{PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT}`.  They are classified only as
**pre-targeted-repair intuitions** and preserved separately from the targeted
provider-backed mapping recorded at `{literature['retrieved_at']}`.  They are
not blind pre-search artifacts: the earlier bounded search had already begun,
their precedence relative to every frontier-search exposure is unknown, and
the timestamp does not establish when an idea first occurred.

The rebase records exact providers, indexes, query IDs, retrieval sessions,
source versions, domains, and transfer limits.  It is deliberately
non-exhaustive: there was no systematic review, full citation-graph closure,
complete proof audit, or peer-validation exercise.  Retrieval shows what pages
and author-stated claims were inspected, not that those claims are correct.
The later six-lane broad capture at `{rel(BROAD_FRONTIER_CAPTURE)}` uses
non-ID-seeded queries and preserves every raw include/exclude disposition.  It
adds surveillance breadth but does not retroactively change the intuition
chronology or establish exhaustiveness.

For central-cycle interoperability, a conservative closed-vocabulary projection emits
`{rel(CANONICAL_LITERATURE_SNAPSHOT)}` as snapshot
`{canonical_snapshot['snapshot_id']}` and
`{rel(CANONICAL_LITERATURE_ASSIMILATION)}` as packet
`{canonical_assimilation['packet_id']}`.  Both validate against the central
literature schemas.  It is explicitly not lossless: provider ranking payloads,
rich retrieval-session structure, and some typed source metadata remain outside
the central schema.  Canonical provenance remains `local_only` and the
active-investment gate remains `blocked_local_only`, because a browser-assisted
external capture is not a receipt-producing search-operator execution.  A
matching central search receipt must independently re-execute the lanes before
novelty, theorem promotion, or active investment can be authorized.

## June 2026 direct challenger

arXiv:2606.19362 is retained with status **unverified_challenger**.  Its abstract
claims a pure four-dimensional SU(N) construction, a uniform transfer-operator
gap, an area law, continuum clustering/string tension, OS reconstruction with a
Hamiltonian gap, regulator universality, and a weak/strong-coupling identity.
Neither arXiv presence nor the journal reference verifies those claims or
changes the official open-target boundary.  The rebase creates six separate
claim-by-claim obligations:

1. audit the exact transfer-operator theorem, assumptions, gauge constraints,
   coupling/volume regime, and uniformity without assuming a gap;
2. audit polymer/character convergence, loop classes, constants, and the route
   from strong coupling to the continuum trajectory;
3. audit every multiscale estimate, regulator-removal step, limiting measure,
   and theory-identity claim;
4. audit the complete OS axioms, vacuum/observable sector, and the precise
   Euclidean-decay-to-Hamiltonian-gap implication;
5. audit the regulator class, Lipschitz/telescoping comparison, uniqueness, and
   universality theorem; and
6. audit weak-coupling entry, asymptotic freedom, phase continuity, and equality
   of observables across the claimed weak/strong constructions.

The obligations are not broadcast to every rival.  The independent claim-effects
oracle maps each claim only to mechanisms that change under its counterfactual:
transfer gap to R02/R08/R10; area law to R02/R07/R10; continuum clustering to
R02/R04/R05/R06/R08/R10; OS/Hamiltonian reconstruction to
R01/R02/R08/R09/R10; universality to R01/R06/R08/R10; and weak/strong identity
to R04/R06/R08/R10.  These mappings reprioritize audits but raise no truth score.

## Independent incumbent-overlap evaluation

The generator's `external_to_incumbent` booleans are candidate assertions, not
evaluation evidence.  `{rel(INCUMBENT_OVERLAP_EVALUATION)}` binds a distinct
evaluator identity to the exact candidate mechanism digest and records typed
primitive, mechanism, endpoint, infrastructure, and ontology overlap.  In
particular R01, R02, R08, and R09 retain explicit endpoint overlap; R02, R03,
R06, R07, R08, and R09 are qualified for material overlap; and R10 is the
incumbent identity control.  The evaluation has no theorem-truth authority.

## Lane-specific genealogy and transfer limits

- R01/R09 now use arXiv:1906.00999 as a **linear** homotopy-AQFT comparator;
  interacting pure Yang-Mills, nonperturbative nets, nuclearity, and a gap remain
  outside its domain.
- R03/R07 now use arXiv:1412.5148 for higher-form symmetry language and
  arXiv:1703.00501 for the theta=pi center/time-reversal anomaly.  Classification
  and vacuum constraints do not generate a quantitative theta=0 mass scale.
- R04/R05 now use arXiv:2006.04987, arXiv:2201.03487, and the current
  arXiv:2503.03060 result for rigorous gauge-orbit/process and renormalisation
  genealogy.  Their 2D/3D and Yang-Mills-Higgs results do not transfer to global
  pure-4D dynamics, hypocoercivity, physical-time decay, or a mass gap.
- R09 uses arXiv:1410.0664 only as a finite-system quantum-recovery theorem.  A
  Yang-Mills application still needs the physical algebra/state factorization,
  gauge constraints, continuum control, and recovery-to-spectrum theorem.
- Related Higgs and abelian sources remain calibration comparators, and the
  withdrawn arXiv:2506.00284 record remains negative-control evidence only.

## Rival conceptual corners to probe aggressively

1. Treat histories or processes, rather than retained boundary states, as the
   primitive object; ask whether Markov sufficiency is the obstruction rather
   than the missing estimate.
2. Treat representation change as the invariant phenomenon and fixed
   representations as gauges; seek a categorical or operational spectral
   quantity that survives RG without defect bookkeeping.
3. Treat topology/information loss as a constructive source of rigidity rather
   than a complement channel to be charged.
4. Reverse the direction from spectral density: characterize which observable
   completeness principle would force the right local conditional geometry.
5. Explore relational temporal coherence that does not factor through a rare
   bad-event field, explicitly confronting Stage 68's hidden-mode counterfamily.
6. Consider whether the desired unification is a theorem about families of
   representations and recovery maps, not one privileged infrared basin.
7. **Structurally external programme:** start from operator-algebraic
   constructive QFT (local observable nets, modular/phase-space nuclearity,
   and representation-independent spectral conditions) and ask whether a
   mass scale can be forced without retained-state kernels, defect fields,
   block RG, or relational-rigidity predicates.

These are high-risk prompts, not endorsed theories.  Each must be rebased
against current literature and matured in an isolated branch before comparison.

## Integration decision

Activate only the three constructive frontier skills that sharpen currently
named conditional inequalities.  Reuse the seventeen already adapted YM
skills.  Keep all ten publication skills external-only.  Use executable tests
as secondary support for the theory-driven discovery cycle, with raw failures
and qualifications visible.
"""
    NORMALIZED_ROOT.mkdir(parents=True, exist_ok=True)
    (NORMALIZED_ROOT / "conceptual_assessment.md").write_text(assessment, encoding="utf-8")
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "conceptual_assessment.md").write_text(assessment, encoding="utf-8")


def write_ym_registry(index: dict[str, dict[str, Any]]) -> None:
    """Declare a target-specific route without mutating generic registries."""

    canonical_snapshot = json.loads(CANONICAL_LITERATURE_SNAPSHOT.read_text(encoding="utf-8"))
    canonical_assimilation = json.loads(
        CANONICAL_LITERATURE_ASSIMILATION.read_text(encoding="utf-8")
    )
    payload = {
        "schema_version": 1,
        "registry_id": "ym-representational-dynamics-20260721",
        "target_scope": TARGET_ID,
        "source_version": VERSION,
        "controller": "reflective-conceptual-discovery",
        "theory_first_order": [
            "current_literature_rebase",
            "conceptual_rival_generation",
            "isolated_hypothesis_maturation",
            "conditional_inequality_proof",
            "secondary_replay_or_simulation_support",
            "independent_frontier_audit",
        ],
        "pre_cycle_hook": {
            "command": (
                "python agentic/scripts/integrate_ym_representational_dynamics_20260721.py "
                "--refresh-normalized --require-literature-after <cycle-date> "
                "--theory-state-digest <canonical-state-digest>"
            ),
            "fixture": rel(DEFAULT_LITERATURE),
            "required": True,
            "authority_boundary": (
                "The dated external-provider capture refreshes causal mappings but remains local_only "
                "until a receipt-backed central literature-search operator independently executes it."
            ),
        },
        "canonical_literature_interop": {
            "snapshot": {
                "path": rel(CANONICAL_LITERATURE_SNAPSHOT),
                "snapshot_id": canonical_snapshot["snapshot_id"],
                "content_digest": canonical_snapshot["content_digest"],
                "theory_state_digest": canonical_snapshot["theory_state_digest"],
                "provenance_mode": canonical_snapshot["provenance_mode"],
            },
            "assimilation": {
                "path": rel(CANONICAL_LITERATURE_ASSIMILATION),
                "packet_id": canonical_assimilation["packet_id"],
                "content_digest": canonical_assimilation["content_digest"],
                "hypothesis_rebase_status": canonical_assimilation["hypothesis_rebase_status"],
                "active_investment_gate": canonical_assimilation["resolution"]["active_investment_gate"],
            },
            "schema_contracts": [
                "agentic/spec/target_literature_search_snapshot.schema.json",
                "agentic/spec/literature_assimilation_packet.schema.json",
            ],
            "claim_authority": "none_without_receipt_backed_search_and_independent_theorem_validation",
        },
        "aggressive_rival_portfolio": {
            "path": rel(NORMALIZED_ROOT / "aggressive_rival_portfolio.json"),
            "incumbent_portfolio": rel(NORMALIZED_ROOT / "hypothesis_portfolio.json"),
            "parallel_ready": True,
            "max_workers": 4,
            "conflict_preserving_reduce": True,
        },
        "active_imported_skills": [
            {
                "skill": skill,
                "local_path": f"skills/yang_mills/{skill}/SKILL.md",
                "source": source_reference(
                    f"11_vscode_codex_skill_bundle/.agents/skills/{skill}/SKILL.md", index
                ),
                "role": "conditional_constructive_frontier",
            }
            for skill in ACTIVE_NEW_SKILLS
        ],
        "reused_existing_skills": list(REUSED_SKILLS),
        "external_only_publication_skills": list(PUBLICATION_SKILLS),
        "replay": {
            "command": "python agentic/scripts/replay_ym_representational_dynamics_20260721.py",
            "role": "secondary_support",
            "source_mutation_forbidden": True,
            "no_xfail_or_suppression": True,
        },
        "claim_ceiling": "C2_restricted_or_C3_explicitly_conditional",
        "non_claims": ["continuum construction", "OS reconstruction", "Hamiltonian mass gap", "Clay solution"],
    }
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None:
        payload["canonical_literature_interop"]["registered_runtime_upgrade"] = runtime_binding
        payload["pre_cycle_hook"]["last_completed_runtime_status"] = "active_current"
        payload["pre_cycle_hook"]["last_completed_runtime_binding"] = rel(
            REGISTERED_RUNTIME_BINDING
        )
    write_json(YM_REGISTRY, payload)


def write_reports(
    manifest: dict[str, Any],
    checksum_report: dict[str, Any],
    active_index: dict[str, Any],
) -> None:
    replay_path = REPORT_ROOT / "replay_report.json"
    replay_status = "pending"
    if replay_path.exists():
        replay_status = json.loads(replay_path.read_text(encoding="utf-8")).get("status", "unknown")
    canonical_snapshot = json.loads(
        CANONICAL_LITERATURE_SNAPSHOT.read_text(encoding="utf-8")
    )
    canonical_assimilation = json.loads(
        CANONICAL_LITERATURE_ASSIMILATION.read_text(encoding="utf-8")
    )
    report = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "source_manifest": rel(IMPORT_ROOT / "immutable_source_manifest.json"),
        "raw_archive_sha256": manifest["raw_archive"]["sha256"],
        "package_checksums": checksum_report,
        "active_snapshot": active_index["summary"],
        "license_status": "unknown",
        "authorship_status": "unknown",
        "upstream_repository_status": "unknown",
        "activated_new_skills": list(ACTIVE_NEW_SKILLS),
        "reused_existing_skills": list(REUSED_SKILLS),
        "external_only_publication_skills": list(PUBLICATION_SKILLS),
        "replay_status": replay_status,
        "conceptual_decision": "incumbent elaboration imported as evidence; reflective plural discovery remains the parent",
        "aggressive_rival_portfolio": {
            "path": rel(NORMALIZED_ROOT / "aggressive_rival_portfolio.json"),
            "structurally_external_rivals": 9,
            "protected_wildcards": 3,
            "conservative_controls": 1,
            "parallel_ready": True,
        },
        "direct_literature_challenger": {
            "source_id": DIRECT_CHALLENGER_ID,
            "status": "unverified_challenger",
            "claim_obligations": 6,
            "effect": "reprioritize theory-collision audits only",
        },
        "canonical_literature_interop": {
            "snapshot_path": rel(CANONICAL_LITERATURE_SNAPSHOT),
            "snapshot_id": canonical_snapshot["snapshot_id"],
            "snapshot_content_digest": canonical_snapshot["content_digest"],
            "assimilation_path": rel(CANONICAL_LITERATURE_ASSIMILATION),
            "assimilation_packet_id": canonical_assimilation["packet_id"],
            "assimilation_content_digest": canonical_assimilation["content_digest"],
            "provenance_mode": canonical_snapshot["provenance_mode"],
            "hypothesis_rebase_status": canonical_assimilation[
                "hypothesis_rebase_status"
            ],
            "active_investment_gate": canonical_assimilation["resolution"][
                "active_investment_gate"
            ],
        },
        "epistemic_boundary": "restricted/conditional evidence only; no continuum Yang--Mills construction or mass-gap proof",
    }
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None:
        report["registered_canonical_runtime"] = runtime_binding
        report["canonical_literature_interop"]["active_runtime_status"] = (
            "active_current"
        )
    write_json(REPORT_ROOT / "integration_report.json", report)
    (REPORT_ROOT / "integration_report.md").write_text(
        "\n".join(
            [
                "# Yang--Mills 2026-07-21 integration report",
                "",
                f"- Target: `{TARGET_ID}`",
                f"- Raw archive: `{manifest['raw_archive']['repo_path']}`",
                f"- SHA-256: `{manifest['raw_archive']['sha256']}`",
                f"- Package checksums: `{checksum_report['verified_count']}/{checksum_report['declared_count']}` verified",
                f"- Filtered snapshot files: `{active_index['summary']['included_files']}`",
                f"- Replay: `{replay_status}`",
                f"- New active skills: `{len(ACTIVE_NEW_SKILLS)}`; reused YM skills: `{len(REUSED_SKILLS)}`",
                f"- Publication skills external-only: `{len(PUBLICATION_SKILLS)}`",
                "- Provenance boundary: authorship, upstream repository, and license are unknown; preserve locally as user-supplied evidence.",
                "- Conceptual decision: this is strong incumbent-program elaboration, not sufficient conceptual plurality.",
                f"- Direct challenger: `{DIRECT_CHALLENGER_ID}` remains `unverified_challenger` with six claim-level audit obligations.",
                f"- Central literature adapter: `{canonical_snapshot['provenance_mode']}` provenance, `{canonical_assimilation['hypothesis_rebase_status']}` rebase, `{canonical_assimilation['resolution']['active_investment_gate']}` investment gate.",
                "- Claim boundary: no continuum construction, OS reconstruction, Hamiltonian gap, or Clay proof.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def integrate(
    source_archive: Path,
    literature_path: Path,
    *,
    refresh_normalized: bool = False,
    require_literature_after: str | None = None,
    theory_state_digest: str | None = None,
) -> dict[str, Any]:
    """Perform an immutable import followed by refreshable evidence normalization."""

    if not source_archive.exists():
        raise IntegrationError(f"missing source archive: {source_archive}")
    source_hash = sha256_file(source_archive)
    if source_hash != EXPECTED_ARCHIVE_SHA256:
        raise IntegrationError(f"source archive hash mismatch: {source_hash}")
    if not literature_path.exists():
        raise IntegrationError(f"missing literature fixture: {rel(literature_path)}")
    literature = json.loads(literature_path.read_text(encoding="utf-8"))
    if not isinstance(literature, dict):
        raise IntegrationError("literature fixture must contain an object")
    validate_literature_snapshot(literature, require_after=require_literature_after)
    validate_frontier_search_capture(_load_json_object(BROAD_FRONTIER_CAPTURE))

    raw_destination = ARCHIVE_ROOT / source_archive.name
    if not refresh_normalized:
        _copy_raw_once(source_archive, raw_destination)
    elif not raw_destination.exists():
        raise IntegrationError("cannot refresh normalized evidence before immutable source import")

    with zipfile.ZipFile(raw_destination) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise IntegrationError(f"zip CRC failure: {bad_member}")
        safe_rows = safe_file_members(archive)
        member_map = {_safe_member_path(info.filename).as_posix(): info for info, _ in safe_rows}
        checksum_report = verify_package_checksums(archive, member_map)
        if checksum_report["declared_count"] != EXPECTED_CHECKSUM_COUNT or not checksum_report["all_ok"]:
            raise IntegrationError(f"package checksum verification failed: {checksum_report}")
        included, excluded = extract_snapshot(archive, safe_rows)

    imported_index = {row["path"]: row for row in included}
    active_digest = sha256_bytes(canonical_bytes([(row["path"], row["sha256"], row["size_bytes"]) for row in included]))
    dispositions: dict[str, int] = {}
    for row in included:
        dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1
    top_level = sorted({PurePosixPath(row["path"]).parts[0] for row in included})
    active_index = {
        "schema_version": 1,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "active_content_digest": active_digest,
        "summary": {
            "included_files": len(included),
            "excluded_files": len(excluded),
            "top_level_siblings": len(top_level),
            "dispositions": dispositions,
        },
        "top_level_entries": top_level,
        "files": included,
        "excluded": excluded,
        "policy": "full safe sibling snapshot; pyc/cache/build/nested archives excluded; activation is disposition-specific",
    }
    active_index_digest = _write_immutable_json(IMPORT_ROOT / "active_index.json", active_index)
    checksum_digest = _write_immutable_json(IMPORT_ROOT / "checksum_report.json", checksum_report)

    old_digest = tree_digest(OLD_IMPORT_ROOT)
    manifest = {
        "schema_version": 1,
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "captured_date": VERSION,
        "source_origin": str(source_archive),
        "raw_archive": {
            "repo_path": rel(raw_destination),
            "sha256": EXPECTED_ARCHIVE_SHA256,
            "size_bytes": raw_destination.stat().st_size,
            "zip_member_count": len(zipfile.ZipFile(raw_destination).infolist()),
            "byte_for_byte_preserved": True,
        },
        "package_checksum_verification": {
            "declared": checksum_report["declared_count"],
            "verified": checksum_report["verified_count"],
            "failed": checksum_report["failed_count"],
            "report_sha256": checksum_digest,
        },
        "active_snapshot": {
            "root": rel(SNAPSHOT_ROOT),
            "content_digest": active_digest,
            "index_sha256": active_index_digest,
            "read_only": True,
            "excluded_policy": "pyc/cache/build/nested archives excluded",
        },
        "preexisting_2026_07_20_import": {"path": rel(OLD_IMPORT_ROOT), "tree_digest": old_digest, "preserved": True},
        "license": {
            "status": "unknown",
            "redistribution_authority": "not_established",
            "use_boundary": "user-supplied local research evidence; do not infer a license",
        },
        "provenance": {
            "authorship_status": "unknown",
            "upstream_repository_status": "unknown",
            "upstream_repository_url": None,
            "inference_boundary": "archive contents and checksums do not establish authorship, ownership, or an upstream repository",
        },
        "epistemic_status": "research programme with finite/restricted and explicitly conditional claims; not a Clay proof",
        "upstream_installer_executed": False,
    }
    manifest_digest = _write_immutable_json(IMPORT_ROOT / "immutable_source_manifest.json", manifest)

    normalize_evidence(
        imported_index,
        literature,
        theory_state_digest=theory_state_digest,
    )
    write_ym_registry(imported_index)
    write_reports(manifest, checksum_report, active_index)
    result = {
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "manifest": rel(IMPORT_ROOT / "immutable_source_manifest.json"),
        "manifest_sha256": manifest_digest,
        "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "checksums": f"{checksum_report['verified_count']}/{checksum_report['declared_count']}",
        "active_files": len(included),
        "excluded_files": len(excluded),
        "active_skills": list(ACTIVE_NEW_SKILLS),
        "publication_external_only": len(PUBLICATION_SKILLS),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--literature-fixture", type=Path, default=DEFAULT_LITERATURE)
    parser.add_argument("--refresh-normalized", action="store_true")
    parser.add_argument("--require-literature-after")
    parser.add_argument(
        "--theory-state-digest",
        help=(
            "Bind the canonical-schema literature adapter to an exact discovery epistemic-state digest. "
            "If omitted, emit a non-authoritative dated adapter template."
        ),
    )
    args = parser.parse_args()
    try:
        integrate(
            args.archive,
            args.literature_fixture,
            refresh_normalized=args.refresh_normalized,
            require_literature_after=args.require_literature_after,
            theory_state_digest=args.theory_state_digest,
        )
    except (IntegrationError, OSError, zipfile.BadZipFile, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
