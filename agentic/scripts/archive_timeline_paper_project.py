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
"""Archive the current timeline-paper build into a stable paper-project folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, slugify, utc_now, write_json


PAPER_JSON = ROOT / "agentic/reports/timeline_paper/latest.json"
PROJECTS_ROOT = ROOT / "agentic/reports/paper_projects"
OUT_INDEX = PROJECTS_ROOT / "index.json"

KNOWN_PROJECT_IDS = {
    "p-vs-np-target": "p-vs-np-transfer-obstruction-certificate",
    "yang-mills-existence-and-mass-gap-target": "yang-mills-wilson-os-timeline-paper",
}

ARTIFACT_GROUPS = {
    "timeline_paper": ROOT / "agentic/reports/timeline_paper",
    "timeline_latex_sections": ROOT / "agentic/reports/timeline_latex_sections",
    "timeline_formal_derivation": ROOT / "agentic/reports/timeline_formal_derivation",
    "timeline_paper_interpretation": ROOT / "agentic/reports/timeline_paper_interpretation",
    "timeline_paper_blueprint": ROOT / "agentic/reports/timeline_paper_blueprint",
    "timeline_paper_sections": ROOT / "agentic/reports/timeline_paper_sections",
    "timeline_paper_diagrams": ROOT / "agentic/reports/timeline_paper_diagrams",
}


def load_json(path: Path) -> dict[str, Any]:
    import json

    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def infer_project_id(paper: dict[str, Any], explicit: str = "") -> str:
    if clean_text(explicit):
        return slugify(explicit)
    target_id = clean_text(paper.get("target_id"))
    if target_id in KNOWN_PROJECT_IDS:
        return KNOWN_PROJECT_IDS[target_id]
    title = clean_text(paper.get("title")) or target_id or "timeline-paper"
    return slugify(title)[:96]


def copy_group(group_name: str, source_dir: Path, project_dir: Path) -> dict[str, str]:
    copied: dict[str, str] = {}
    if not source_dir.exists():
        return copied
    target_dir = project_dir / group_name
    target_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_dir.glob("latest*")):
        if source.is_file():
            target = target_dir / source.name
            shutil.copy2(source, target)
            suffix = source.suffix.lstrip(".")
            key = suffix if source.stem == "latest" and suffix else source.name.replace(".", "_")
            copied[key] = rel(target)
    return copied


def build_index(projects_root: Path) -> dict[str, Any]:
    projects = []
    for manifest in sorted(projects_root.glob("*/latest.json")):
        data = load_json(manifest)
        if data.get("paper_project_id"):
            projects.append(
                {
                    "paper_project_id": data.get("paper_project_id"),
                    "target_id": data.get("target_id"),
                    "title": data.get("title"),
                    "manifest": rel(manifest),
                    "updated_utc": data.get("archived_utc"),
                }
            )
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "status": "paper_project_index_ready",
        "project_count": len(projects),
        "projects": projects,
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    paper = manifest.get("project_artifacts", {}).get("timeline_paper", {})
    lines = [
        f"# Paper Project: {manifest['paper_project_id']}",
        "",
        f"- Target: `{manifest['target_id']}`",
        f"- Title: {manifest['title']}",
        f"- Project root: `{manifest['project_root']}`",
        f"- TeX: `{paper.get('tex', '')}`",
        f"- PDF: `{paper.get('pdf', '')}`",
        "",
        "## Compatibility Pointers",
        "",
        *[f"- `{item}`" for item in manifest.get("compatibility_pointers", [])],
        "",
        "## Archived Groups",
        "",
        *[f"- `{name}`: {len(paths)} artifact(s)" for name, paths in manifest.get("project_artifacts", {}).items()],
        "",
    ]
    return "\n".join(lines)


def archive_project(project_id: str = "") -> dict[str, Any]:
    paper = load_json(PAPER_JSON)
    if not paper:
        raise SystemExit(f"missing paper JSON: {rel(PAPER_JSON)}")
    selected = infer_project_id(paper, project_id)
    project_dir = PROJECTS_ROOT / selected
    project_dir.mkdir(parents=True, exist_ok=True)

    artifacts = {
        group_name: copy_group(group_name, source_dir, project_dir)
        for group_name, source_dir in ARTIFACT_GROUPS.items()
    }
    manifest = {
        "version": 1,
        "archived_utc": utc_now(),
        "status": "paper_project_archive_ready",
        "paper_project_id": selected,
        "target_id": clean_text(paper.get("target_id")),
        "title": clean_text(paper.get("title")),
        "paper_id": clean_text(paper.get("paper_id")),
        "project_root": rel(project_dir),
        "source_latest_json": rel(PAPER_JSON),
        "compatibility_pointers": [
            rel(ROOT / "agentic/reports/timeline_paper/latest.json"),
            rel(ROOT / "agentic/reports/timeline_paper/latest.tex"),
            rel(ROOT / "agentic/reports/timeline_paper/latest.pdf"),
        ],
        "project_artifacts": artifacts,
        "validation_handoff": "python agentic/scripts/validate_paper_project_archive.py",
    }
    write_json(project_dir / "latest.json", manifest)
    (project_dir / "latest.md").write_text(render_markdown(manifest), encoding="utf-8")
    write_json(OUT_INDEX, build_index(PROJECTS_ROOT))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-project-id", default="", help="Optional stable paper-project id.")
    args = parser.parse_args()
    manifest = archive_project(args.paper_project_id)
    print(f"Wrote {manifest['project_root']}/latest.json")
    print(f"Wrote {rel(OUT_INDEX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
