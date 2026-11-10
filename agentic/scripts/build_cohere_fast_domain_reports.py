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
"""Build deterministic cohere-fast YM review and minimal-closure projections."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def dump_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> int:
    manifest = json.loads((ROOT / "agentic/imports/cohere_fast/source_manifest.json").read_text())
    collisions = json.loads((ROOT / "agentic/imports/cohere_fast/collision_report.json").read_text())
    bundle = yaml.safe_load((ROOT / "agentic/registries/domain_skill_bundles.yaml").read_text())["bundles"][0]
    source = {Path(row["path"]).parent.name: row for row in manifest["members"]
              if "/skills/programs/yang-mills/" in "/" + row["path"] and row["path"].endswith("/SKILL.md")}
    rows = []
    for item in collisions["skills"]:
        skill = item["source_skill"]
        src = source[skill]
        rows.append({
            "skill_id": skill, "decision": item["decision"],
            "runtime_mode": "domain_private_adapter", "owner": "cohere_fast/ym",
            "input_type": "DomainEvidencePacket", "output_type": "DomainEvidencePacket",
            "claim_ceiling": "candidate", "source_member": src["path"],
            "source_member_sha256": src["sha256"], "adapted_path": item["adapted_path"],
            "existing_path": item["existing_path"], "license_policy": "independent-rewrite-only",
        })
    skill_map = {"schema_version": "1.0", "workflow_id": "cohere_fast", "domain_id": "ym", "skills": rows}
    map_path = ROOT / "agentic/registries/cohere_fast_ym_skill_map.yaml"
    map_path.write_text(yaml.safe_dump(skill_map, sort_keys=False))
    dump_json(ROOT / "agentic/reports/cohere_fast_ym_skill_review/latest.json", {
        "schema_version": "1.0", "archive_sha256": "sha256:" + manifest["archive_sha256"],
        "license_status": manifest["license_status"], "skill_count": len(rows),
        "collision_count": sum(bool(r["existing_path"]) for r in rows), "overwrite_count": 0,
        "contract_complete_count": sum((ROOT / r["adapted_path"] / "SKILL.md").is_file() for r in rows),
        "skills": rows,
    })
    adapters = yaml.safe_load((ROOT / "agentic/registries/cohere_fast_skill_adapters.yaml").read_text())
    closure = {
        "schema_version": "1.0", "policy": "minimal-v1-only",
        "domain_skills": bundle["allowed_skills"], "shared_adapters": adapters["adapters"],
        "unresolved_references": [], "wholesale_import": False,
        "rejected_capabilities": ["source TDR control plane", "source CLI", "source SQLite state", "compatibility aliases", "unselected programme catalogs"],
    }
    dump_json(ROOT / "agentic/reports/cohere_fast_dependency_closure/latest.json", closure)
    print(f"built YM review for {len(rows)} skills and {len(adapters['adapters'])} shared adapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
