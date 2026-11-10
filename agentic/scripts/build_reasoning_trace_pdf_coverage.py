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
"""Compute PDF projection visibility independently from source trace coverage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_public_reasoning_trace_pdf import (
    EXPECTED_STEMS, GENERATED, _inventory_ids, _norm, _required_pdf_strings,
    companion_paths, extract_pdf_text, packet_semantic_ids, semantic_visible,
)


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "agentic/reports/reasoning_trace_pdf_coverage"


def build_coverage(packet: dict[str, Any], inventory: dict[str, Any], pdf_text: str) -> dict[str, Any]:
    normalized_pdf = _norm(pdf_text)
    inventory_ids = _inventory_ids(inventory)
    by_lane: dict[str, Any] = {}
    all_rows: list[dict[str, Any]] = []
    for lane, identifiers in packet_semantic_ids(packet).items():
        rows = []
        for semantic_id in sorted(identifiers):
            row = {
                "semantic_id": semantic_id,
                "inventory_disposition": "visible" if semantic_id in inventory_ids else "missing",
                "pdf_visibility": "visible" if semantic_visible(semantic_id, pdf_text) else "missing",
            }
            rows.append(row); all_rows.append(row)
        by_lane[lane] = {
            "total": len(rows), "inventory_visible": sum(row["inventory_disposition"] == "visible" for row in rows),
            "pdf_visible": sum(row["pdf_visibility"] == "visible" for row in rows), "items": rows,
        }
    sentinel_rows = [
        {"location": location, "value": value, "pdf_visibility": "visible" if semantic_visible(value, pdf_text) else "missing"}
        for location, value in _required_pdf_strings(packet)
    ]
    total = len(all_rows)
    sentinel_total = len(sentinel_rows)
    identity = packet.get("identity", {})
    return {
        "schema_version": "1.0", "identity": identity,
        "source_coverage": dict(packet.get("coverage", {})),
        "projection_coverage": {
            "inventory_total": total,
            "inventory_visible": sum(row["inventory_disposition"] == "visible" for row in all_rows),
            "pdf_id_total": total,
            "pdf_id_visible": sum(row["pdf_visibility"] == "visible" for row in all_rows),
            "pdf_sentinel_total": sentinel_total,
            "pdf_sentinel_visible": sum(row["pdf_visibility"] == "visible" for row in sentinel_rows),
            "complete": all(row["inventory_disposition"] == "visible" and row["pdf_visibility"] == "visible" for row in all_rows)
                and all(row["pdf_visibility"] == "visible" for row in sentinel_rows),
        },
        "by_lane": by_lane, "semantic_sentinels": sentinel_rows,
        "accessibility_conformance": {"pdf_ua": "not_run", "tagged_pdf": "not_run"},
    }


def render_markdown(reports: list[dict[str, Any]]) -> str:
    lines = ["# Reasoning-trace PDF visibility", "", "PDF visibility is measured independently from source, HTML, and print-inventory coverage.", "", "| Workflow/profile | Inventory IDs | PDF IDs | PDF sentinels | Complete |", "|---|---:|---:|---:|---|"]
    for report in reports:
        identity = report["identity"]; projection = report["projection_coverage"]
        label = str(identity.get("workflow_id", "")) + (f" / {identity['profile_id']}" if identity.get("profile_id") else "")
        lines.append(f"| {label} | {projection['inventory_visible']}/{projection['inventory_total']} | {projection['pdf_id_visible']}/{projection['pdf_id_total']} | {projection['pdf_sentinel_visible']}/{projection['pdf_sentinel_total']} | {'yes' if projection['complete'] else 'no'} |")
    lines.extend(["", "Formal PDF/UA and tagged-PDF conformance: **not run**. Selectable-text and semantic visibility checks do not imply conformance.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=REPORT_DIR)
    parser.add_argument("--check", action="store_true", help="fail if any projection is incomplete")
    args = parser.parse_args()
    reports = []
    for stem in sorted(EXPECTED_STEMS):
        paths = companion_paths(stem)
        if not all(paths[key].is_file() for key in ("packet", "inventory", "pdf")):
            print(f"missing PDF coverage inputs for {stem}")
            return 1
        reports.append(build_coverage(
            json.loads(paths["packet"].read_text(encoding="utf-8")),
            json.loads(paths["inventory"].read_text(encoding="utf-8")),
            extract_pdf_text(paths["pdf"]),
        ))
    payload = {"schema_version": "1.0", "reports": reports, "all_complete": all(r["projection_coverage"]["complete"] for r in reports)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "latest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.output_dir / "latest.md").write_text(render_markdown(reports), encoding="utf-8")
    print(f"wrote PDF coverage for {len(reports)} reports; complete={payload['all_complete']}")
    return 1 if args.check and not payload["all_complete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
