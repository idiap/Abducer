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
"""Validate the immutable, replayed, theory-first YM21 integration."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from agentic_common import ROOT, rel
from agentic.discovery.literature import (
    LANE_TYPES,
    validate_assimilation as validate_canonical_assimilation,
    validate_snapshot as validate_canonical_snapshot,
)
from integrate_ym_representational_dynamics_20260721 import (
    ACTIVE_NEW_SKILLS,
    BROAD_FRONTIER_CAPTURE,
    CANONICAL_LITERATURE_ASSIMILATION,
    CANONICAL_LITERATURE_SNAPSHOT,
    DIRECT_CHALLENGER_ID,
    EXPECTED_ARCHIVE_SHA256,
    EXPECTED_CHECKSUM_COUNT,
    IMPORT_ROOT,
    INCUMBENT_OVERLAP_EVALUATION,
    LANE_GENEALOGY_SOURCE_IDS,
    NORMALIZED_ROOT,
    OLD_IMPORT_ROOT,
    PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT,
    PUBLICATION_SKILLS,
    REGISTERED_RUNTIME_BINDING,
    REGISTERED_RUNTIME_ROOT,
    REPORT_ROOT,
    REUSED_SKILLS,
    RIVAL_SEEDS,
    SNAPSHOT_ROOT,
    TARGET_ID,
    VERSION,
    YM_REGISTRY,
    canonical_bytes,
    registered_runtime_binding_if_present,
    sha256_bytes,
    sha256_file,
    tree_digest,
    validate_direct_claim_theory_mappings,
    validate_frontier_search_capture,
    validate_incumbent_overlap_evaluation,
    validate_literature_snapshot,
)
from validate_ym_canonical_parent_cycle_20260721 import (
    validate as validate_canonical_parent_cycle,
)


TODO_DECK = ROOT / "agentic/todos/ym_representational_dynamics_20260721_todos.yaml"
LITERATURE_FIXTURE = ROOT / "agentic/evals/ym_representational_dynamics_20260721/literature_snapshot_current.json"
EXPECTATIONS = ROOT / "agentic/evals/ym_representational_dynamics_20260721/integration_expectations.json"
CONCEPT_CASES = ROOT / "agentic/evals/ym_representational_dynamics_20260721/conceptual_integration_cases.jsonl"
RIVAL_SCHEMA = ROOT / "agentic/evals/ym_representational_dynamics_20260721/aggressive_rival_portfolio.schema.json"
QUALIFICATION_EXPECTATION = ROOT / "agentic/evals/ym_representational_dynamics_20260721/stage70_expected_qualification.json"


class ValidationError(RuntimeError):
    """Raised on the first integration contract violation."""


def parse_timestamp(raw: str) -> dt.datetime:
    """Parse a timezone-aware RFC-3339 timestamp for chronology checks."""

    try:
        parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValidationError(f"invalid timestamp: {raw!r}") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"timestamp lacks timezone: {raw!r}")
    return parsed.astimezone(dt.timezone.utc)


def require(path: Path) -> Path:
    if not path.exists():
        raise ValidationError(f"missing required artifact: {rel(path)}")
    return path


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(require(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValidationError(f"{rel(path)} must contain an object")
    return payload


def validate_lock(path: Path) -> str:
    digest = sha256_file(require(path))
    lock = require(path.with_suffix(path.suffix + ".sha256")).read_text(encoding="utf-8").strip()
    expected = f"{digest}  {path.name}"
    if lock != expected:
        raise ValidationError(f"digest lock mismatch: {rel(path)}")
    return digest


def validate_source() -> tuple[dict[str, Any], dict[str, Any]]:
    require(IMPORT_ROOT / "README.md")
    manifest_path = IMPORT_ROOT / "immutable_source_manifest.json"
    checksum_path = IMPORT_ROOT / "checksum_report.json"
    index_path = IMPORT_ROOT / "active_index.json"
    manifest = load_object(manifest_path)
    checksum = load_object(checksum_path)
    active_index = load_object(index_path)
    validate_lock(manifest_path)
    validate_lock(checksum_path)
    validate_lock(index_path)
    if manifest.get("target_id") != TARGET_ID or manifest.get("source_version") != VERSION:
        raise ValidationError("immutable source manifest scope mismatch")
    raw = manifest.get("raw_archive", {})
    archive_path = ROOT / str(raw.get("repo_path", ""))
    if sha256_file(require(archive_path)) != EXPECTED_ARCHIVE_SHA256:
        raise ValidationError("raw archive is not byte-for-byte identical to the accepted source")
    if raw.get("sha256") != EXPECTED_ARCHIVE_SHA256 or raw.get("byte_for_byte_preserved") is not True:
        raise ValidationError("raw archive manifest boundary is incomplete")
    if checksum.get("declared_count") != EXPECTED_CHECKSUM_COUNT or checksum.get("verified_count") != EXPECTED_CHECKSUM_COUNT:
        raise ValidationError("package checksum count is not 1389/1389")
    if checksum.get("all_ok") is not True or checksum.get("failed_count") != 0:
        raise ValidationError("package checksum report contains a failure")
    license_packet = manifest.get("license", {})
    if license_packet.get("status") != "unknown" or license_packet.get("redistribution_authority") != "not_established":
        raise ValidationError("unknown upstream license must remain explicit")
    provenance = manifest.get("provenance", {})
    if provenance.get("authorship_status") != "unknown" or provenance.get("upstream_repository_status") != "unknown" or provenance.get("upstream_repository_url") is not None:
        raise ValidationError("unknown authorship and upstream-repository provenance must remain explicit")
    if manifest.get("upstream_installer_executed") is not False:
        raise ValidationError("upstream installer execution is forbidden")
    old = manifest.get("preexisting_2026_07_20_import", {})
    if not OLD_IMPORT_ROOT.exists() or tree_digest(OLD_IMPORT_ROOT) != old.get("tree_digest"):
        raise ValidationError("the preexisting 2026-07-20 import changed")

    files = active_index.get("files")
    excluded = active_index.get("excluded")
    if not isinstance(files, list) or not isinstance(excluded, list):
        raise ValidationError("active index must contain included and excluded rows")
    paths = {row.get("path") for row in files if isinstance(row, dict)}
    if len(paths) != len(files):
        raise ValidationError("active index has duplicate or malformed paths")
    forbidden = [
        path
        for path in paths
        if isinstance(path, str)
        and (
            "__pycache__" in path.split("/")
            or ".pytest_cache" in path.split("/")
            or Path(path).suffix.lower() in {".pyc", ".pyo", ".zip", ".aux", ".log", ".out", ".toc"}
        )
    ]
    if forbidden:
        raise ValidationError(f"active index contains excluded byproducts: {forbidden[:5]}")
    excluded_reasons = {row.get("reason") for row in excluded if isinstance(row, dict)}
    if not {"cache_or_build_directory", "nested_archive"}.issubset(excluded_reasons):
        raise ValidationError("active index does not account for cache/build and nested-archive exclusions")
    stage_numbers = {
        int(match.group(1))
        for name in active_index.get("top_level_entries", [])
        if (match := re.match(r"^(\d{2})_", str(name)))
    }
    if stage_numbers != set(range(1, 80)):
        raise ValidationError(f"active sibling layout is incomplete: missing {sorted(set(range(1, 80)) - stage_numbers)}")
    for row in files:
        path = SNAPSHOT_ROOT / row["path"]
        if sha256_file(require(path)) != row["sha256"] or path.stat().st_size != row["size_bytes"]:
            raise ValidationError(f"active snapshot drift: {row['path']}")
        if path.stat().st_mode & 0o222:
            raise ValidationError(f"active source is writable: {row['path']}")
    active_digest = sha256_bytes(
        canonical_bytes([(row["path"], row["sha256"], row["size_bytes"]) for row in files])
    )
    if active_digest != active_index.get("active_content_digest") or active_digest != manifest["active_snapshot"]["content_digest"]:
        raise ValidationError("active snapshot content digest mismatch")
    return manifest, active_index


def _iter_source_refs(value: Any) -> Iterable[dict[str, str]]:
    if isinstance(value, dict):
        if set(("source_path", "source_sha256")).issubset(value):
            yield {"source_path": str(value["source_path"]), "source_sha256": str(value["source_sha256"])}
        for child in value.values():
            yield from _iter_source_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_source_refs(child)


def validate_normalized_evidence() -> None:
    portfolio = load_object(NORMALIZED_ROOT / "hypothesis_portfolio.json")
    evidence = load_object(NORMALIZED_ROOT / "evidence_ledger.json")
    publication = load_object(NORMALIZED_ROOT / "publication_capability_map.json")
    for payload in (portfolio, evidence, publication):
        if payload.get("target_id") != TARGET_ID or payload.get("source_version") != VERSION:
            raise ValidationError("normalized evidence scope mismatch")
        for ref in _iter_source_refs(payload):
            path = ROOT / ref["source_path"]
            if sha256_file(require(path)) != ref["source_sha256"]:
                raise ValidationError(f"normalized source reference drift: {ref['source_path']}")
    hypotheses = portfolio.get("hypotheses")
    if not isinstance(hypotheses, list) or [row.get("hypothesis_id") for row in hypotheses] != [f"H{i}" for i in range(1, 11)]:
        raise ValidationError("normalized H1--H10 portfolio is incomplete")
    if any(row.get("status") != "incumbent_program_branch" for row in hypotheses):
        raise ValidationError("imported hypotheses must retain incumbent-program ancestry")
    nonclaims = " ".join(portfolio.get("non_claims", [])).lower()
    for marker in ("continuum", "os reconstruction", "mass gap"):
        if marker not in nonclaims:
            raise ValidationError(f"portfolio missing non-claim: {marker}")
    records = evidence.get("records", [])
    if {row.get("evidence_id") for row in records} != {"YM21-E52", "YM21-E78", "YM21-E79"}:
        raise ValidationError("Stage 52/78/79 evidence normalization is incomplete")
    if publication.get("policy") != "external_only_until_separately_scoped_and_current-literature-grounded":
        raise ValidationError("publication capability policy drift")
    publication_rows = publication.get("skills", [])
    if {row.get("skill") for row in publication_rows} != set(PUBLICATION_SKILLS) or any(row.get("local_activation") for row in publication_rows):
        raise ValidationError("all ten publication skills must remain external-only")

    rival = load_object(NORMALIZED_ROOT / "aggressive_rival_portfolio.json")
    schema = load_object(RIVAL_SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(rival), key=lambda item: list(item.path))
    if errors:
        raise ValidationError(f"aggressive rival portfolio schema failure: {errors[0].message}")
    digest_payload = dict(rival)
    observed_digest = digest_payload.pop("content_digest")
    if observed_digest != sha256_bytes(canonical_bytes(digest_payload)):
        raise ValidationError("aggressive rival portfolio content digest mismatch")
    overlap_evaluation = load_object(INCUMBENT_OVERLAP_EVALUATION)
    try:
        validate_incumbent_overlap_evaluation(overlap_evaluation, rival)
    except Exception as exc:
        raise ValidationError(f"independent incumbent-overlap evaluation failed: {exc}") from exc
    overlap_binding = rival.get("incumbent_overlap_evaluation", {})
    for key in (
        "evaluation_id",
        "generator_identity",
        "evaluator_identity",
        "candidate_set_digest",
        "content_digest",
    ):
        if overlap_binding.get(key) != overlap_evaluation.get(key):
            raise ValidationError(f"incumbent-overlap portfolio binding drift: {key}")
    if (
        overlap_binding.get("path") != rel(INCUMBENT_OVERLAP_EVALUATION)
        or overlap_binding.get("truth_authority") != "none"
        or overlap_binding.get("evaluator_identity") == overlap_binding.get("generator_identity")
    ):
        raise ValidationError("incumbent overlap is self-attested or granted truth authority")

    canonical_snapshot = load_object(CANONICAL_LITERATURE_SNAPSHOT)
    canonical_assimilation = load_object(CANONICAL_LITERATURE_ASSIMILATION)
    try:
        validate_canonical_snapshot(canonical_snapshot)
        validate_canonical_assimilation(
            canonical_assimilation, snapshot=canonical_snapshot
        )
    except Exception as exc:
        raise ValidationError(
            f"central literature interoperability contract failed: {exc}"
        ) from exc
    lane_receipts = canonical_snapshot["lane_receipts"]
    if (
        canonical_snapshot.get("target_id") != TARGET_ID
        or canonical_snapshot.get("provenance_mode") != "local_only"
        or {row.get("lane_type") for row in lane_receipts} != set(LANE_TYPES)
        or len(lane_receipts) != len(LANE_TYPES)
        or any(row.get("execution_mode") != "local_only" for row in lane_receipts)
    ):
        raise ValidationError(
            "external browser capture was laundered into receipt-backed central provenance"
        )
    if (
        canonical_assimilation.get("hypothesis_rebase_status")
        != "provisional_local_only"
        or canonical_assimilation.get("resolution", {}).get(
            "active_investment_gate"
        )
        != "blocked_local_only"
    ):
        raise ValidationError(
            "manual literature booleans opened a central investment or novelty gate"
        )
    interop = rival.get("canonical_literature_interop", {})
    expected_interop = {
        "snapshot_path": rel(CANONICAL_LITERATURE_SNAPSHOT),
        "snapshot_id": canonical_snapshot["snapshot_id"],
        "snapshot_content_digest": canonical_snapshot["content_digest"],
        "assimilation_path": rel(CANONICAL_LITERATURE_ASSIMILATION),
        "assimilation_packet_id": canonical_assimilation["packet_id"],
        "assimilation_content_digest": canonical_assimilation["content_digest"],
        "theory_state_digest": canonical_snapshot["theory_state_digest"],
        "provenance_mode": "local_only",
        "hypothesis_rebase_status": "provisional_local_only",
        "active_investment_gate": "blocked_local_only",
    }
    for key, expected in expected_interop.items():
        if interop.get(key) != expected:
            raise ValidationError(
                f"rival portfolio central-literature binding drift: {key}"
            )
    if (
        interop.get("projection_mode")
        != "conservative_closed_vocabulary_projection"
        or len(interop.get("projection_omissions", [])) < 3
        or "no lossless-equivalence claim" not in interop.get("authority_boundary", "")
    ):
        raise ValidationError("central-schema adapter overstates projection fidelity")
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None:
        stored_binding = load_object(REGISTERED_RUNTIME_BINDING)
        if stored_binding != runtime_binding:
            raise ValidationError("stored registered-runtime binding is stale")
        if interop.get("registered_runtime_upgrade") != runtime_binding:
            raise ValidationError("rival portfolio omits the active-current registered runtime")
    if canonical_assimilation.get("theory_state_digest") != canonical_snapshot.get(
        "theory_state_digest"
    ):
        raise ValidationError("canonical literature artifacts bind different theory states")

    rivals = [row for row in rival["hypotheses"] if row["portfolio_role"] == "structurally_external_rival"]
    controls = [row for row in rival["hypotheses"] if row["portfolio_role"] == "conservative_control"]
    if len(rivals) < 8 or len(controls) != 1 or any(not row["structural_externality"]["external_to_incumbent"] for row in rivals):
        raise ValidationError("aggressive portfolio lacks eight structurally external rivals plus one control")
    wildcard_ids = set(rival["protected_wildcard_ids"])
    if len(wildcard_ids) < 2 or not wildcard_ids.issubset({row["hypothesis_id"] for row in rivals}):
        raise ValidationError("aggressive portfolio lacks two protected external wildcards")
    literature = load_object(LITERATURE_FIXTURE)
    sources_by_id = {row["source_id"]: row for row in literature["sources"]}
    source_ids = set(sources_by_id)
    seeds_by_id = {seed["id"]: seed for seed in RIVAL_SEEDS}
    snapshot_digest = sha256_bytes(canonical_bytes(literature))
    for row in rival["hypotheses"]:
        seed = seeds_by_id.get(row["hypothesis_id"])
        if seed is None:
            raise ValidationError(f"unrecognized rival seed: {row['hypothesis_id']}")
        intuition = row["pre_targeted_repair_intuition"]
        if (
            intuition["text"] != seed["intuition"]
            or intuition["captured_at"] != PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT
            or intuition["preserved_verbatim_before_source_mapping"] is not True
            or intuition.get("full_frontier_search_precedence") != "unknown"
            or "not a pre-search claim" not in intuition["temporal_boundary"]
        ):
            raise ValidationError(f"pre-targeted-repair intuition boundary drift: {row['hypothesis_id']}")
        risk = row["risk_reward"]
        if set(risk) != {"probability_of_truth", "value_if_right", "learning_value_if_false", "maturation_cost"}:
            raise ValidationError(f"risk/reward axes collapsed: {row['hypothesis_id']}")
        rebase = row["literature_rebase"]
        expected_source_ids = [item[0] for item in seed["sources"]]
        if rebase.get("mapping_phase") != "targeted_repair_after_bounded_search" or rebase.get(
            "snapshot_digest"
        ) != snapshot_digest:
            raise ValidationError(f"targeted-repair mapping boundary drift: {row['hypothesis_id']}")
        if parse_timestamp(intuition["captured_at"]) >= parse_timestamp(rebase["mapped_at"]):
            raise ValidationError(
                f"intuition text does not precede the targeted repair: {row['hypothesis_id']}"
            )
        if rebase["source_ids"] != expected_source_ids or not set(
            rebase["source_ids"]
        ).issubset(source_ids):
            raise ValidationError(f"unknown literature source in rival: {row['hypothesis_id']}")
        if {effect["source_id"] for effect in rebase["causal_effects"]} != set(rebase["source_ids"]):
            raise ValidationError(f"causal literature mapping incomplete: {row['hypothesis_id']}")
        if rebase["priority_effect"].get("changed_by_source_ids") != rebase[
            "source_ids"
        ]:
            raise ValidationError(
                f"priority effect is not source-complete: {row['hypothesis_id']}"
            )
        if len(rebase.get("required_revisions", [])) < 2:
            raise ValidationError(
                f"literature did not cause explicit revisions: {row['hypothesis_id']}"
            )
        for effect in rebase["causal_effects"]:
            source = sources_by_id[effect["source_id"]]
            if (
                effect.get("source_domain") != source["domain"]
                or effect.get("transfer_boundary") != source["transfer_boundary"]
                or effect.get("claim_status") != source["claim_status"]
            ):
                raise ValidationError(
                    f"lossy claim-level source mapping: {row['hypothesis_id']} / {effect['source_id']}"
                )
        if DIRECT_CHALLENGER_ID in rebase["source_ids"]:
            challenger_effect = next(
                item
                for item in rebase["causal_effects"]
                if item["source_id"] == DIRECT_CHALLENGER_ID
            )
            if (
                challenger_effect.get("claim_status") != "unverified_challenger"
                or challenger_effect.get("effect_type") != "reprioritize"
            ):
                raise ValidationError(
                    f"direct challenger received claim authority: {row['hypothesis_id']}"
                )
    for priority_id in ("YM21-R02", "YM21-R08", "YM21-R10"):
        row = next(item for item in rival["hypotheses"] if item["hypothesis_id"] == priority_id)
        if DIRECT_CHALLENGER_ID not in row["literature_rebase"]["source_ids"]:
            raise ValidationError(f"direct challenger missing priority collision: {priority_id}")

    mappings = canonical_assimilation.get("theory_mappings", [])
    challenger_audits = sources_by_id[DIRECT_CHALLENGER_ID]["claim_audit"]
    challenger_mappings = [
        mapping for mapping in mappings if mapping.get("source_id") == DIRECT_CHALLENGER_ID
    ]
    try:
        validate_direct_claim_theory_mappings(mappings, literature)
    except Exception as exc:
        raise ValidationError(f"independent claim-specific mapping oracle failed: {exc}") from exc
    if len(challenger_mappings) != len(challenger_audits):
        raise ValidationError("central adapter collapsed direct-challenger claim obligations")
    audit_claims = {row["author_stated_claim"] for row in challenger_audits}
    if (
        {row.get("exact_claim") for row in challenger_mappings} != audit_claims
        or any(
            row.get("confidence") != "low"
            or row.get("relation") != "leaves_open"
            or row.get("event_type") != "reprioritize"
            for row in challenger_mappings
        )
    ):
        raise ValidationError("central challenger mappings promoted an unverified claim")
    plan = rival["parallel_maturation_plan"]
    if len(plan["branches"]) != len(rival["hypotheses"]) or plan["max_workers"] != 4 or plan["merge_policy"]["automatic_truth_selection"] is not False:
        raise ValidationError("aggressive rival portfolio is not safely parallel-ready")


def validate_literature() -> str:
    fixture = load_object(LITERATURE_FIXTURE)
    validate_literature_snapshot(fixture)
    broad_capture = load_object(BROAD_FRONTIER_CAPTURE)
    validate_frontier_search_capture(broad_capture)
    try:
        validate_literature_snapshot(fixture, require_after="2026-07-22")
    except Exception:
        pass
    else:
        raise ValidationError("pre-cycle literature hook did not fail on a later required cutoff")
    rebase = load_object(NORMALIZED_ROOT / "literature_rebase.json")
    digest = sha256_bytes(canonical_bytes(fixture))
    provenance = rebase.get("search_provenance", {})
    if (
        provenance.get("snapshot_digest") != digest
        or rebase.get("required_before_every_target_cycle") is not True
        or provenance.get("snapshot_kind") != "provider_backed_web_capture"
        or provenance.get("provider_backed") is not True
        or provenance.get("live_recency_claim") is not True
        or provenance.get("exhaustive_coverage_claim") is not False
        or provenance.get("peer_validation_claim") is not False
    ):
        raise ValidationError("literature rebase is not bound to the current fixture and every target cycle")
    if rebase.get("portfolio_effect", {}).get("promotion") != "none":
        raise ValidationError("current literature does not justify imported claim promotion")
    withdrawn = [row for row in rebase.get("sources", []) if row.get("source_status") == "withdrawn"]
    if not withdrawn or any(row.get("disposition") != "excluded" for row in withdrawn):
        raise ValidationError("withdrawn literature is not preserved as exclusion evidence")

    source_ids = {row["source_id"] for row in fixture["sources"]}
    required_sources = {DIRECT_CHALLENGER_ID, *LANE_GENEALOGY_SOURCE_IDS}
    if not required_sources.issubset(source_ids):
        raise ValidationError("dated literature snapshot dropped challenger or lane genealogy")
    challenger = next(
        row for row in fixture["sources"] if row["source_id"] == DIRECT_CHALLENGER_ID
    )
    audits = challenger.get("claim_audit", [])
    if (
        challenger.get("source_status") != "unverified_challenger"
        or challenger.get("claim_status") != "unverified_challenger"
        or len(audits) != 6
        or any(
            item.get("verification_status") != "unverified"
            or not item.get("required_obligation")
            for item in audits
        )
    ):
        raise ValidationError("direct challenger was not preserved as six unverified obligations")
    lane_rebase = rebase.get("rival_lane_rebase", [])
    if len(lane_rebase) != len(RIVAL_SEEDS) or {
        row.get("hypothesis_id") for row in lane_rebase
    } != {seed["id"] for seed in RIVAL_SEEDS}:
        raise ValidationError("literature rebase does not causally cover every rival lane")
    if any(
        row.get("full_frontier_search_precedence") != "unknown"
        or "pre_search_captured_at" in row
        or "post_search_mapped_at" in row
        for row in lane_rebase
    ):
        raise ValidationError("literature rebase launders pre-targeted-repair chronology into pre-search chronology")
    broad_binding = rebase.get("search_provenance", {}).get("broad_frontier_capture", {})
    if (
        broad_binding.get("path") != rel(BROAD_FRONTIER_CAPTURE)
        or broad_binding.get("capture_id") != broad_capture["capture_id"]
        or broad_binding.get("content_digest") != sha256_file(BROAD_FRONTIER_CAPTURE)
        or "does not retroactively" not in broad_binding.get("chronology_effect", "")
    ):
        raise ValidationError("broad frontier capture is not honestly bound into the rebase")
    direct = rebase.get("portfolio_effect", {}).get("direct_challenger", {})
    if (
        direct.get("source_id") != DIRECT_CHALLENGER_ID
        or direct.get("status") != "unverified_challenger"
        or direct.get("claim_obligation_count") != 6
        or "without claim promotion" not in direct.get("effect", "")
    ):
        raise ValidationError("direct challenger portfolio effect overstates verification")

    snapshot = load_object(CANONICAL_LITERATURE_SNAPSHOT)
    assimilation = load_object(CANONICAL_LITERATURE_ASSIMILATION)
    interop = rebase.get("canonical_literature_interop", {})
    if (
        interop.get("snapshot_id") != snapshot["snapshot_id"]
        or interop.get("snapshot_content_digest") != snapshot["content_digest"]
        or interop.get("assimilation_packet_id") != assimilation["packet_id"]
        or interop.get("assimilation_content_digest") != assimilation["content_digest"]
        or interop.get("provenance_mode") != "local_only"
        or interop.get("active_investment_gate") != "blocked_local_only"
    ):
        raise ValidationError("dated rebase and central interoperability artifacts disagree")
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None:
        if (
            rebase.get("active_canonical_literature_status") != "active_current"
            or rebase.get("registered_runtime_upgrade") != runtime_binding
            or "registered runtime" not in rebase.get("authority_boundary", "")
            or "active_current" not in rebase.get("authority_boundary", "")
        ):
            raise ValidationError(
                "normalized literature rebase falsely reports only local_only after registered execution"
            )
    return digest


def validate_conceptual_assessment() -> None:
    raw_text = require(NORMALIZED_ROOT / "conceptual_assessment.md").read_text(encoding="utf-8").lower()
    text = " ".join(raw_text.split())
    required_markers = (
        "incumbent elaboration, not plural conceptual discovery",
        "reflective conceptual parent loop",
        "rival conceptual corners",
        "high-risk prompts, not endorsed theories",
        "structurally external programme",
        "secondary support",
        "unverified_challenger",
        "arxiv:2606.19362",
        "non-exhaustive",
        "blocked_local_only",
        "claim-by-claim",
        "pre-targeted-repair intuitions",
        "not blind pre-search artifacts",
        "conservative closed-vocabulary projection",
        "independent incumbent-overlap evaluation",
    )
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise ValidationError(f"conceptual assessment missing judgments: {missing}")
    numbered = re.findall(r"(?m)^\d+\. ", raw_text)
    if len(numbered) < 6:
        raise ValidationError("conceptual assessment has fewer than six rival corners")
    cases = require(CONCEPT_CASES).read_text(encoding="utf-8").splitlines()
    if len([json.loads(line) for line in cases if line.strip()]) < 4:
        raise ValidationError("conceptual integration evaluation corpus is incomplete")


def validate_skills_and_registry() -> None:
    registry = load_object(YM_REGISTRY)
    if registry.get("target_scope") != TARGET_ID or registry.get("source_version") != VERSION:
        raise ValidationError("YM-specific registry scope mismatch")
    active = registry.get("active_imported_skills", [])
    if {row.get("skill") for row in active} != set(ACTIVE_NEW_SKILLS) or len(active) != 3:
        raise ValidationError("YM21 must activate exactly three imported skills")
    if set(registry.get("reused_existing_skills", [])) != set(REUSED_SKILLS):
        raise ValidationError("YM21 registry does not maximize reuse of the seventeen existing skills")
    if set(registry.get("external_only_publication_skills", [])) != set(PUBLICATION_SKILLS):
        raise ValidationError("YM21 publication quarantine is incomplete")
    if registry.get("controller") != "reflective-conceptual-discovery" or registry.get("replay", {}).get("role") != "secondary_support":
        raise ValidationError("theory-first controller or experiment/replay subordination drift")
    canonical_snapshot = load_object(CANONICAL_LITERATURE_SNAPSHOT)
    canonical_assimilation = load_object(CANONICAL_LITERATURE_ASSIMILATION)
    interop = registry.get("canonical_literature_interop", {})
    snapshot_binding = interop.get("snapshot", {})
    assimilation_binding = interop.get("assimilation", {})
    if (
        snapshot_binding.get("snapshot_id") != canonical_snapshot["snapshot_id"]
        or snapshot_binding.get("content_digest") != canonical_snapshot["content_digest"]
        or snapshot_binding.get("theory_state_digest")
        != canonical_snapshot["theory_state_digest"]
        or snapshot_binding.get("provenance_mode") != "local_only"
        or assimilation_binding.get("packet_id")
        != canonical_assimilation["packet_id"]
        or assimilation_binding.get("content_digest")
        != canonical_assimilation["content_digest"]
        or assimilation_binding.get("hypothesis_rebase_status")
        != "provisional_local_only"
        or assimilation_binding.get("active_investment_gate")
        != "blocked_local_only"
        or interop.get("claim_authority")
        != "none_without_receipt_backed_search_and_independent_theorem_validation"
    ):
        raise ValidationError("YM registry central-literature binding or authority drift")
    pre_cycle = registry.get("pre_cycle_hook", {})
    if (
        "--theory-state-digest <canonical-state-digest>"
        not in pre_cycle.get("command", "")
        or "local_only" not in pre_cycle.get("authority_boundary", "")
    ):
        raise ValidationError("YM pre-cycle hook is not bound to an exact theory state")
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None and (
        interop.get("registered_runtime_upgrade") != runtime_binding
        or pre_cycle.get("last_completed_runtime_status") != "active_current"
        or pre_cycle.get("last_completed_runtime_binding")
        != rel(REGISTERED_RUNTIME_BINDING)
    ):
        raise ValidationError("YM registry omits the accepted active-current runtime")
    markers = (
        TARGET_ID,
        "Abducer Integration Guards",
        "current target literature rebase",
        "not as plural conceptual discovery",
        "subordinate",
        f"/{VERSION}/active_snapshot/",
        "anti-definitionality",
        "declarative-learning",
    )
    for skill in ACTIVE_NEW_SKILLS:
        skill_path = require(ROOT / f"skills/yang_mills/{skill}/SKILL.md")
        text = skill_path.read_text(encoding="utf-8")
        if not re.search(rf"(?m)^name:\s*{re.escape(skill)}\s*$", text):
            raise ValidationError(f"skill frontmatter mismatch: {skill}")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise ValidationError(f"{skill} missing integration guards: {missing}")
        require(skill_path.parent / "agents/openai.yaml")
    for skill in PUBLICATION_SKILLS:
        if (ROOT / f"skills/yang_mills/{skill}/SKILL.md").exists():
            raise ValidationError(f"publication skill was activated locally: {skill}")
    orchestrator = require(ROOT / "skills/yang_mills/ym-run-clay-program/SKILL.md").read_text(encoding="utf-8")
    missing = [skill for skill in ACTIVE_NEW_SKILLS if skill not in orchestrator]
    if missing:
        raise ValidationError(f"YM orchestrator does not route the three new skills: {missing}")


def validate_replay() -> dict[str, Any]:
    report = load_object(REPORT_ROOT / "replay_report.json")
    if report.get("status") != "passed_with_qualified_stage70_drift":
        raise ValidationError(f"unexpected complete replay status: {report.get('status')}")
    if report.get("complete_dynamic_discovery") is not True or report.get("executed_test_file_count") != report.get("discovered_test_file_count"):
        raise ValidationError("not every dynamically discovered test file was replayed")
    if report.get("source_unchanged") is not True or report.get("source_read_only") is not True or report.get("temporary_workspaces") is not True:
        raise ValidationError("replay did not preserve read-only source isolation")
    if report.get("no_observed_skip_or_xfail") is not True or any(report.get("suppression_policy", {}).values()):
        raise ValidationError("skip, xfail, or suppression appeared in replay")
    stages = report.get("stages", [])
    stage70 = next((row for row in stages if row.get("stage") == "70_h3_exact_multistar"), None)
    if not stage70:
        raise ValidationError("Stage 70 is absent from replay")
    if stage70.get("raw_status") != "failed" or stage70.get("counts", {}).get("passed") != 13 or stage70.get("counts", {}).get("failed") != 1:
        raise ValidationError("Stage 70 raw 13-pass/1-fail outcome was not preserved")
    if stage70.get("effective_status") != "qualified_noncanonical_witness_drift":
        raise ValidationError("Stage 70 exact qualification is absent")
    unexpected = [row.get("stage") for row in stages if row is not stage70 and row.get("raw_status") != "passed"]
    if unexpected:
        raise ValidationError(f"unqualified raw stage failures: {unexpected}")
    expected = load_object(QUALIFICATION_EXPECTATION)
    qualification = report.get("stage70_qualification", {})
    if qualification.get("accepted") is not True or [row.get("path") for row in qualification.get("differences", [])] != expected["allowed_semantic_diff_paths"]:
        raise ValidationError("Stage 70 qualification exceeds the one allowed semantic path")
    normalized = load_object(NORMALIZED_ROOT / "stage70_qualification.json")
    if normalized.get("accepted") is not True or normalized.get("raw_test_result") != {"passed": 13, "failed": 1}:
        raise ValidationError("normalized Stage 70 qualification is incomplete")
    return report


def validate_todos(*, require_resolved: bool) -> list[str]:
    rows = json.loads(require(TODO_DECK).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or [row.get("id") for row in rows] != [f"YM21-{index:03d}" for index in range(1, 11)]:
        raise ValidationError("YM21 TODO deck must contain ordered YM21-001 through YM21-010")
    if require_resolved:
        unresolved = [row.get("id") for row in rows if row.get("status") != "resolved"]
        if unresolved:
            raise ValidationError(f"YM21 TODOs are not resolved: {unresolved}")
    for row in rows:
        if not row.get("evidence") or not row.get("acceptance_criteria") or not row.get("required_artifact") or not row.get("validation_commands"):
            raise ValidationError(f"TODO lacks evidence contract: {row.get('id')}")
        for raw_path in row["required_artifact"]:
            path = ROOT / raw_path
            require(path)
    return [row["id"] for row in rows]


def validate(*, require_resolved: bool = True) -> None:
    expectations = load_object(EXPECTATIONS)
    if expectations.get("archive_sha256") != EXPECTED_ARCHIVE_SHA256 or expectations.get("package_checksum_count") != EXPECTED_CHECKSUM_COUNT:
        raise ValidationError("evaluation expectations drifted from accepted source")
    validate_source()
    validate_normalized_evidence()
    validate_literature()
    validate_conceptual_assessment()
    validate_skills_and_registry()
    # The broad import/replay validator is not a substitute for proof that the
    # imported material actually passed through the six-operator theory-first
    # parent cycle.  Keep that exact content-addressed runtime in the aggregate
    # gate so a stale or fallback-only conceptual packet cannot close YM21.
    validate_canonical_parent_cycle()
    replay = validate_replay()
    validate_todos(require_resolved=require_resolved)
    report = load_object(REPORT_ROOT / "integration_report.json")
    if (
        report.get("replay_status") != replay["status"]
        or report.get("license_status") != "unknown"
        or report.get("authorship_status") != "unknown"
        or report.get("upstream_repository_status") != "unknown"
    ):
        raise ValidationError("integration report is stale relative to replay or license boundary")
    runtime_binding = registered_runtime_binding_if_present()
    if runtime_binding is not None and (
        report.get("registered_canonical_runtime") != runtime_binding
        or report.get("canonical_literature_interop", {}).get(
            "active_runtime_status"
        )
        != "active_current"
    ):
        raise ValidationError("integration report omits the accepted active-current runtime")


def validate_card(card_id: str, *, require_resolved: bool = False) -> None:
    """Run the smallest evidence-complete validator set for one YM21 card.

    Card-scoped validation prevents ten broad ``--allow-open-todos`` invocations
    from masquerading as ten different acceptance arguments.  Shared
    dependencies are intentionally repeated where a later card's claim relies
    on them; YM21-010 remains the aggregate integration gate.
    """

    validators = {
        "YM21-001": (validate_source,),
        "YM21-002": (validate_source,),
        "YM21-003": (validate_replay,),
        "YM21-004": (validate_replay,),
        "YM21-005": (validate_source, validate_normalized_evidence),
        "YM21-006": (validate_literature, validate_canonical_parent_cycle),
        "YM21-007": (
            validate_conceptual_assessment,
            validate_canonical_parent_cycle,
        ),
        "YM21-008": (validate_skills_and_registry,),
        "YM21-009": (validate_normalized_evidence,),
    }
    if card_id == "YM21-010":
        validate(require_resolved=require_resolved)
        return
    selected = validators.get(card_id)
    if selected is None:
        raise ValidationError(f"unknown YM21 card: {card_id}")
    for validator in selected:
        validator()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-open-todos", action="store_true")
    parser.add_argument(
        "--card",
        choices=[f"YM21-{index:03d}" for index in range(1, 11)],
        help="run a focused evidence-complete validator for one TODO card",
    )
    args = parser.parse_args()
    try:
        if args.card:
            validate_card(
                args.card,
                require_resolved=not args.allow_open_todos,
            )
        else:
            validate(require_resolved=not args.allow_open_todos)
    except (ValidationError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    suffix = f" card {args.card}" if args.card else " integration"
    print(f"validated YM 2026-07-21 representational-dynamics{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
