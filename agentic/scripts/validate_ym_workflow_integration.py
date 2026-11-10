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
"""Validate the target-scoped Yang-Mills representational-dynamics integration."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from discovery_marathon_common import read_report_target_id


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
IMPORT_ROOT = ROOT / "agentic/external/yang_mills_representational_dynamics/2026-07-20"
REPORT_ROOT = ROOT / "agentic/reports/ym_representational_dynamics_integration"
TARGET_REPORT_ROOT = ROOT / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target"
PROOF_OBJECTS = TARGET_REPORT_ROOT / "proof_objects/ym_representational_dynamics_objects.json"
SKILL_ROOT = ROOT / "skills/yang_mills"
DISPATCH = ROOT / "agentic/registries/discovery_marathon_skill_dispatch.yaml"
TASK_REGISTRY = ROOT / "registry/tasks/discovery-marathon/task_registry.json"
SMOKE_MANIFEST = ROOT / "agentic/logs/discovery_marathon_jobs/ym-overlay-smoke/manifest.json"

YM_SKILLS = [
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
]


def require(path: Path) -> None:
    if not path.exists():
        fail(f"missing required YM integration artifact: {rel(path)}")


def validate_zip_integrity(manifest: dict[str, Any]) -> None:
    archives = manifest.get("archives", {})
    for key in ["research_archive", "skill_archive"]:
        path = Path(clean_text(archives.get(key, {}).get("path")))
        if not path.exists():
            fail(f"{key} source archive missing: {path}")
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
        if bad is not None:
            fail(f"{key} has bad zip member: {bad}")


def validate_sources() -> None:
    manifest_path = IMPORT_ROOT / "source_manifest.json"
    checksum_path = IMPORT_ROOT / "checksum_report.json"
    source_index_path = REPORT_ROOT / "source_index.json"
    for path in [manifest_path, checksum_path, source_index_path]:
        require(path)
    manifest = load_json_object(manifest_path)
    checksum = load_json_object(checksum_path)
    source_index = load_json_object(source_index_path)
    if clean_text(manifest.get("target_id")) != TARGET_ID:
        fail("YM source manifest target_id mismatch")
    if "does not prove the Clay" not in clean_text(manifest.get("epistemic_status")):
        fail("YM source manifest must state the non-proof boundary")
    if not checksum.get("all_ok"):
        fail("YM package checksum report is not all_ok")
    counts = source_index.get("summary_counts", {})
    if counts.get("pdfs") != 7 or counts.get("tests") != 4 or counts.get("theorem_dependency_graphs") != 3:
        fail(f"unexpected YM source-index counts: {counts}")
    validate_zip_integrity(manifest)


def validate_tests() -> None:
    report = load_json_object(REPORT_ROOT / "test_report.json")
    if report.get("status") != "passed":
        fail("YM restricted-model tests are not passing")
    if report.get("test_count") != 31:
        fail(f"expected 31 YM restricted-model tests, found {report.get('test_count')}")
    if "do not certify the Clay target" not in clean_text(report.get("epistemic_boundary")):
        fail("YM test report must preserve restricted-model boundary")


def validate_skills() -> None:
    found = sorted(path.parent.name for path in SKILL_ROOT.glob("*/SKILL.md"))
    if found != sorted(YM_SKILLS):
        fail(f"expected 17 adapted YM skills, found {found}")
    for skill in YM_SKILLS:
        path = SKILL_ROOT / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        if not re.search(rf"^name:\s*{re.escape(skill)}\s*$", text, re.MULTILINE):
            fail(f"{rel(path)} missing matching frontmatter name")
        required = [
            TARGET_ID,
            "Abducer Integration Guards",
            "anti-definitionality",
            "declarative learning",
            "efficient representation requirements",
            "four-cycle",
        ]
        missing = [marker for marker in required if marker not in text]
        if missing:
            fail(f"{rel(path)} missing guard markers: {missing}")
        require(SKILL_ROOT / skill / "agents/openai.yaml")
    require(SKILL_ROOT / "agents/openai.yaml")


def validate_dispatch_and_registry() -> None:
    dispatch = load_json_object(DISPATCH)
    phases = dispatch.get("phases", [])
    overlay = next((phase for phase in phases if phase.get("phase") == "yang_mills_representational_dynamics_overlay"), None)
    if not overlay:
        fail("dispatch registry missing YM overlay phase")
    if clean_text(overlay.get("target_scope")) != TARGET_ID:
        fail("YM overlay phase must be target-scoped")
    if sorted(overlay.get("required_skills", [])) != sorted(YM_SKILLS):
        fail("YM overlay phase does not require exactly the 17 adapted skills")
    registry = load_json_object(TASK_REGISTRY)
    declared = {row.get("name") for row in registry.get("generated_skills", []) + registry.get("reference_skills", [])}
    missing = sorted(set(YM_SKILLS) - declared)
    if missing:
        fail(f"task registry does not declare YM skills: {missing}")
    workflows = registry.get("visible_workflows", [])
    overlay_workflow = next((row for row in workflows if row.get("name") == "ym-representational-dynamics-overlay"), None)
    if not overlay_workflow:
        fail("task registry missing visible YM overlay workflow")
    if "agentic/scripts/validate_ym_workflow_integration.py" not in overlay_workflow.get("validators", []):
        fail("YM overlay workflow must include its validator")


def validate_proof_objects() -> None:
    payload = load_json_object(PROOF_OBJECTS)
    rows = payload.get("proof_objects", [])
    if not isinstance(rows, list) or len(rows) < 25:
        fail("YM proof-object deck is unexpectedly small")
    for row in rows:
        if clean_text(row.get("target_id")) != TARGET_ID:
            fail(f"proof object target mismatch: {row.get('proof_object_id')}")
        if clean_text(row.get("claim_level")) == "C6" and clean_text(row.get("status")) != "open":
            fail(f"C6 proof object must remain open: {row.get('proof_object_id')}")
        if not row.get("non_claims"):
            fail(f"proof object missing non_claims: {row.get('proof_object_id')}")
        if not row.get("demotion_trigger"):
            fail(f"proof object missing demotion trigger: {row.get('proof_object_id')}")


def validate_reports() -> None:
    for path in [
        REPORT_ROOT / "source_index.md",
        REPORT_ROOT / "skill_adaptation_report.md",
        REPORT_ROOT / "dispatch_overlay_report.md",
        REPORT_ROOT / "prompt_integration_report.md",
        REPORT_ROOT / "report_integration_report.md",
        REPORT_ROOT / "validator_report.md",
        REPORT_ROOT / "smoke_cycle_report.md",
        REPORT_ROOT / "timeline_events.json",
        TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.json",
        TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.html",
        TARGET_REPORT_ROOT / "result_atlas_update.json",
        ROOT / "agentic/reports/results_ellaboration/yang_mills_representational_dynamics_subgoal_decision.md",
    ]:
        require(path)
    overlay = load_json_object(TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.json")
    if clean_text(overlay.get("target_id")) != TARGET_ID:
        fail("YM overlay report target_id mismatch")
    declared = read_report_target_id(TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.html")
    if declared != TARGET_ID:
        fail("YM overlay HTML missing target meta")
    for key in ["latest.json", "latest.md", "latest.html", "full_timeline.html"]:
        path = TARGET_REPORT_ROOT / key
        require(path)
        declared_target = read_report_target_id(path)
        if declared_target != TARGET_ID:
            fail(f"{rel(path)} declares `{declared_target or 'unknown'}`, expected `{TARGET_ID}`")


def validate_smoke_and_docs() -> None:
    smoke = load_json_object(SMOKE_MANIFEST)
    if clean_text(smoke.get("target_id")) != TARGET_ID or smoke.get("status") != "completed":
        fail("YM smoke manifest must be completed and target-scoped")
    if "C6 blocked" not in clean_text(smoke.get("frontier_audit_outcome")):
        fail("YM smoke manifest must include conservative frontier audit status")
    docs = [
        ROOT / "KB/yang-mills-existence-and-mass-gap.kb.md",
        ROOT / "docs/operations/discovery-marathon-operations.md",
        ROOT / "docs/operations/target-navigation-runbook.md",
    ]
    for path in docs:
        require(path)
        text = path.read_text(encoding="utf-8")
        if "Yang-Mills representational dynamics overlay" not in text:
            fail(f"{rel(path)} missing YM overlay documentation marker")


def main() -> int:
    validate_sources()
    validate_tests()
    validate_skills()
    validate_dispatch_and_registry()
    validate_proof_objects()
    validate_reports()
    validate_smoke_and_docs()
    print("validated Yang-Mills representational-dynamics workflow integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
