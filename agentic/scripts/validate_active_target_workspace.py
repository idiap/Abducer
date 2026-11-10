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

"""Validate that latest workflow state belongs to the active target."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, kb_ref_from_path, load_json_object, rel, repo_path, write_json


REPORT_JSON = ROOT / "agentic/reports/stale_workflows/latest.json"
REPORT_MD = ROOT / "agentic/reports/stale_workflows/latest.md"
HISTORICAL_TARGET_MARKERS = [
    "p-vs-np-target",
    "p-vs-np",
    "hille-yosida-theorem",
]


def load_optional_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_json_object(path)


def target_marker_in_path(path: Path) -> str:
    raw = rel(path).lower()
    for marker in HISTORICAL_TARGET_MARKERS:
        if marker in raw:
            return marker
    return ""


def jsonl_target_ids(path: Path) -> set[str]:
    ids = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            ids.add("<malformed-jsonl>")
            continue
        target_id = payload.get("target_id")
        if isinstance(target_id, str):
            ids.add(target_id)
    return ids


def file_contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-target-id", help="Optional target_id that must be active.")
    args = parser.parse_args()

    current_path = ROOT / "agentic/state/current_target.json"
    if not current_path.exists():
        fail("missing active target state: agentic/state/current_target.json")
    target = load_json_object(current_path)
    target_id = str(target.get("target_id", ""))
    if not target_id:
        fail("active target state is missing target_id")
    if args.expected_target_id and target_id != args.expected_target_id:
        fail(f"active target mismatch: expected {args.expected_target_id}, found {target_id}")

    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    graph_path = ROOT / "agentic/state/dependency_graphs" / f"{kb_ref}.json"
    closure_path = ROOT / "agentic/reports/dependency_closure" / f"{kb_ref}.md"
    frontier_path = ROOT / "agentic/state/dependency_frontier.json"
    release_path = ROOT / "agentic/reports/releases/latest.md"
    hegelian_path = ROOT / "artifacts/hegelian/hypothesis_exploration_map.json"
    skill_log_path = ROOT / "agentic/traces/skill_applications/ITER-0001.jsonl"
    hegelian_log_path = ROOT / "agentic/logs/hegelian-conceptual-refinement.jsonl"
    monitor_packet_path = ROOT / "agentic/reports/reasoning_monitor/latest.json"
    monitor_html_path = ROOT / "agentic/reports/reasoning_monitor/latest.html"

    findings: list[dict[str, str]] = []
    active_checks = []

    graph = load_optional_object(graph_path)
    if not graph:
        findings.append({"severity": "critical", "path": rel(graph_path), "message": "missing active dependency graph"})
    elif graph.get("target_id") != target_id:
        findings.append({"severity": "critical", "path": rel(graph_path), "message": f"graph target_id is {graph.get('target_id')}, expected {target_id}"})
    active_checks.append({"path": rel(graph_path), "status": "present" if graph else "missing"})

    frontier = load_optional_object(frontier_path)
    if not frontier:
        findings.append({"severity": "critical", "path": rel(frontier_path), "message": "missing dependency frontier"})
    elif frontier.get("target_id") != target_id:
        findings.append({"severity": "critical", "path": rel(frontier_path), "message": f"frontier target_id is {frontier.get('target_id')}, expected {target_id}"})
    active_checks.append({"path": rel(frontier_path), "status": "present" if frontier else "missing"})

    if not closure_path.exists():
        findings.append({"severity": "critical", "path": rel(closure_path), "message": "missing active dependency closure report"})
    active_checks.append({"path": rel(closure_path), "status": "present" if closure_path.exists() else "missing"})

    if not file_contains(release_path, f"Target ID: `{target_id}`"):
        findings.append({"severity": "critical", "path": rel(release_path), "message": "latest release report does not name active target"})
    active_checks.append({"path": rel(release_path), "status": "target-matched" if file_contains(release_path, f"Target ID: `{target_id}`") else "target-mismatch"})

    hegelian = load_optional_object(hegelian_path)
    if hegelian and hegelian.get("target_id") != target_id:
        findings.append({"severity": "critical", "path": rel(hegelian_path), "message": f"hypothesis exploration target_id is {hegelian.get('target_id')}, expected {target_id}"})
    active_checks.append({"path": rel(hegelian_path), "status": "target-matched" if hegelian.get("target_id") == target_id else "target-mismatch"})

    for log_path in [skill_log_path, hegelian_log_path]:
        ids = jsonl_target_ids(log_path)
        if ids and ids != {target_id}:
            findings.append({"severity": "critical", "path": rel(log_path), "message": f"log target_ids are {sorted(ids)}, expected only {target_id}"})
        active_checks.append({"path": rel(log_path), "status": "target-matched" if ids == {target_id} else "target-mismatch"})

    monitor_packet = load_optional_object(monitor_packet_path)
    if monitor_packet:
        packet_target_id = monitor_packet.get("target", {}).get("target_id")
        if packet_target_id != target_id:
            findings.append({"severity": "critical", "path": rel(monitor_packet_path), "message": f"monitor packet target_id is {packet_target_id}, expected {target_id}"})
        active_checks.append({"path": rel(monitor_packet_path), "status": "target-matched" if packet_target_id == target_id else "target-mismatch"})
    else:
        active_checks.append({"path": rel(monitor_packet_path), "status": "missing"})

    if monitor_html_path.exists():
        text = monitor_html_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'<script id="monitor-data" type="application/json">(.*?)</script>', text, re.DOTALL)
        html_target_id = ""
        if match:
            try:
                embedded = json.loads(match.group(1))
                html_target_id = str(embedded.get("target", {}).get("target_id", ""))
            except json.JSONDecodeError:
                html_target_id = "<invalid-json>"
        if html_target_id != target_id:
            findings.append({"severity": "critical", "path": rel(monitor_html_path), "message": f"monitor HTML embedded target_id is {html_target_id or '<missing>'}, expected {target_id}"})
        active_checks.append({"path": rel(monitor_html_path), "status": "target-matched" if html_target_id == target_id else "target-mismatch"})
    else:
        active_checks.append({"path": rel(monitor_html_path), "status": "missing"})

    historical = []
    stale_active_manifests = []
    for root in [ROOT / "artifacts", ROOT / "agentic/reports/dependency_closure", ROOT / "registry/tasks"]:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            marker = target_marker_in_path(path)
            if marker and marker not in {target_id, kb_ref}:
                historical.append({"path": rel(path), "marker": marker, "status": "historical-not-active"})
                if path.name == "task_registry.json":
                    manifest = load_json_object(path)
                    if manifest.get("status") == "active":
                        stale_active_manifests.append(rel(path))
    for manifest_path in stale_active_manifests:
        findings.append(
            {
                "severity": "critical",
                "path": manifest_path,
                "message": "target-specific historical workflow manifest is still marked active",
            }
        )

    report = {
        "version": 1,
        "active_target_id": target_id,
        "active_kb_ref": kb_ref,
        "critical_findings": sum(1 for row in findings if row["severity"] == "critical"),
        "findings": findings,
        "active_checks": active_checks,
        "historical_artifacts": historical[:200],
        "historical_artifact_count": len(historical),
    }
    write_json(REPORT_JSON, report)
    lines = [
        "# Stale Workflow Preflight",
        "",
        f"- Active target: `{target_id}`",
        f"- Active KB ref: `{kb_ref}`",
        f"- Critical active-state findings: {report['critical_findings']}",
        f"- Historical non-active artifacts observed: {len(historical)}",
        "",
        "## Active Checks",
        "",
    ]
    for row in active_checks:
        lines.append(f"- `{row['path']}`: {row['status']}")
    lines.extend(["", "## Findings", ""])
    if not findings:
        lines.append("None.")
    for finding in findings:
        lines.append(f"- `{finding['severity']}` `{finding['path']}`: {finding['message']}")
    lines.extend(["", "## Historical Artifacts", ""])
    if not historical:
        lines.append("None.")
    for row in historical[:40]:
        lines.append(f"- `{row['path']}` ({row['marker']}): {row['status']}")
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"validated active target workspace for {target_id}; critical findings={report['critical_findings']}")
    return 1 if report["critical_findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
