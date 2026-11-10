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

"""Archive top-level legacy report files that no longer match the current hub contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from generate_report_hub import LEGACY_REPORT_STEMS
from generate_report_hub import REPO_ROOT
from generate_report_hub import SUPPORTED_FORMATS


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _inventory_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    return artifacts_dir / "legacy-report-inventory.json", artifacts_dir / "legacy-report-inventory.md"


def discover_legacy_reports(artifacts_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(artifacts_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_FORMATS:
            continue
        if path.stem not in LEGACY_REPORT_STEMS:
            continue
        rows.append(
            {
                "name": path.name,
                "stem": path.stem,
                "suffix": path.suffix.lower(),
                "reason": "Superseded by the current canonical report contract and excluded from the main report hub.",
            }
        )
    return rows


def archive_legacy_reports(artifacts_dir: Path) -> dict[str, Any]:
    archive_dir = artifacts_dir / "legacy-reports"
    archive_dir.mkdir(parents=True, exist_ok=True)
    discovered = discover_legacy_reports(artifacts_dir)
    archived: list[dict[str, str]] = []
    for row in discovered:
        source = artifacts_dir / row["name"]
        destination = archive_dir / row["name"]
        if destination.exists():
            destination.unlink()
        source.replace(destination)
        archived.append(
            {
                **row,
                "source_path": str(source),
                "archived_path": str(destination),
            }
        )

    inventory = {
        "metadata": {
            "artifacts_dir": str(artifacts_dir),
            "archived_count": len(archived),
            "legacy_stems": sorted(LEGACY_REPORT_STEMS),
        },
        "archived_reports": archived,
    }
    output_json, output_md = _inventory_paths(artifacts_dir)
    output_json.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Legacy Report Inventory",
        "",
        f"- Archived reports: {len(archived)}",
        f"- Legacy stems: {', '.join(sorted(LEGACY_REPORT_STEMS))}",
        "",
    ]
    if not archived:
        lines.append("- No legacy report files were present.")
        lines.append("")
    else:
        for row in archived:
            lines.extend(
                [
                    f"## {row['name']}",
                    "",
                    f"- Reason: {row['reason']}",
                    f"- Archived path: {row['archived_path']}",
                    "",
                ]
            )
    output_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return inventory


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    args = ap.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (REPO_ROOT / artifacts_dir).resolve()
    if not artifacts_dir.exists():
        raise SystemExit(f"[ERROR] Artifacts directory does not exist: {artifacts_dir}")

    inventory = archive_legacy_reports(artifacts_dir)
    output_json, output_md = _inventory_paths(artifacts_dir)
    print(f"[OK] Archived legacy reports: {inventory['metadata']['archived_count']}")
    print(f"[OK] Wrote inventory JSON: {output_json}")
    print(f"[OK] Wrote inventory Markdown: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
