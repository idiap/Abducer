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
"""Build or validate the isolated cohere-fast release scorecard."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
REPORT_JSON = ROOT / "agentic/reports/cohere_fast_release/latest.json"
REPORT_MD = ROOT / "agentic/reports/cohere_fast_release/latest.md"

REQUIRED = {
    "source_manifest": "agentic/imports/cohere_fast/source_manifest.json",
    "source_dispositions": "agentic/imports/cohere_fast/dispositions.json",
    "collision_report": "agentic/imports/cohere_fast/collision_report.json",
    "isolation_contract": "agentic/spec/cohere_fast_isolation_contract.yaml",
    "invocation_schema": "agentic/spec/cohere_fast_invocation.schema.json",
    "domain_registry": "agentic/registries/domain_skill_bundles.yaml",
    "parent_contract": "agentic/registries/cohere_fast_workflow_contracts.yaml",
    "subworkflows": "agentic/registries/cohere_fast_subworkflows.yaml",
    "ym_workflow": "agentic/registries/cohere_fast_ym_workflow.yaml",
    "artifact_schema": "agentic/spec/cohere_fast_artifacts.schema.json",
    "status_crosswalk": "agentic/registries/cohere_fast_status_crosswalk.yaml",
    "runner": "agentic/orchestration/cohere_fast_runner.py",
    "trace_adapter": "agentic/scripts/reasoning_trace_adapters/cohere_fast.py",
    "task_projection": "registry/tasks/cohere-fast/task_registry.json",
    "live_trace_test": "tests/integration/test_cohere_fast_ym_lifecycle.py",
    "noninterference_test": "tests/integration/test_cohere_fast_noninterference.py",
    "documentation": "docs/workflows/cohere-fast.md",
}


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    checks = []
    for check_id, relative in REQUIRED.items():
        path = ROOT / relative
        checks.append({"id": check_id, "status": "pass" if path.is_file() else "fail", "path": relative,
                       "digest": digest(path) if path.is_file() else None})
    registry_path = ROOT / REQUIRED["domain_registry"]
    registry = load(registry_path) if registry_path.is_file() else {}
    ym = next((row for row in registry.get("bundles", []) if row.get("id") == "ym"), {})
    checks.extend([
        {"id": "default_off", "status": "pass" if ym and ym.get("enabled") is False else "fail",
         "detail": "The domain route remains disabled until source redistribution authority is resolved."},
        {"id": "isolated_root", "status": "pass" if str(ym.get("artifact_prefix", "")).startswith("cohere-fast/ym/") else "fail"},
        {"id": "domain_skill_count", "status": "pass" if len(ym.get("allowed_skills", [])) >= 30 else "fail",
         "observed": len(ym.get("allowed_skills", []))},
    ])
    source_path = ROOT / REQUIRED["source_manifest"]
    source = load(source_path) if source_path.is_file() else {}
    license_status = source.get("license_status", source.get("authorization", {}).get("license_status", "unknown"))
    checks.append({"id": "source_license", "status": "pass" if license_status in {"licensed", "explicitly_authorized"} else "blocked",
                   "observed": license_status, "detail": "No license file was detected in the supplied archive; redistribution stays disabled."})
    failures = [row["id"] for row in checks if row["status"] == "fail"]
    blocked = [row["id"] for row in checks if row["status"] == "blocked"]
    return {
        "schema_version": "1.0.0", "workflow_id": "cohere_fast", "domain_id": "ym",
        "release_enabled": not failures and not blocked and bool(ym.get("enabled")),
        "disposition": "blocked" if failures or blocked else "ready_but_disabled",
        "checks": checks, "failed_checks": failures, "blocked_checks": blocked,
        "rollback": {"scope": "cohere-fast registry entries, projections, and active route only", "preserve_historical_receipts": True},
    }


def render_md(payload: dict) -> str:
    lines = ["# Cohere-fast release gate", "", f"Disposition: **{payload['disposition']}**", "",
             "The workflow is isolated and default-off. A valid artifact or event digest establishes integrity only, not scientific correctness.", "",
             "| Check | Status | Detail |", "|---|---|---|"]
    for row in payload["checks"]:
        detail = row.get("detail") or row.get("path") or str(row.get("observed", ""))
        lines.append(f"| {row['id']} | {row['status']} | {detail} |")
    header = "\n".join(
        line.removeprefix("# ")
        for line in Path(__file__).read_text(encoding="utf-8").splitlines()
        if line.startswith("# SPDX-")
        or line == "# Neuro-symbolic AI Group"
    )
    return "<!--\n" + header + "\n-->\n" + "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = build()
    if args.write:
        REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        REPORT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        REPORT_MD.write_text(render_md(payload), encoding="utf-8")
    elif not REPORT_JSON.is_file() or load(REPORT_JSON) != payload:
        raise SystemExit("stale cohere-fast release report; run with --write")
    if payload["failed_checks"]:
        raise SystemExit("cohere-fast release structural checks failed: " + ", ".join(payload["failed_checks"]))
    print(json.dumps({"disposition": payload["disposition"], "blocked": payload["blocked_checks"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
