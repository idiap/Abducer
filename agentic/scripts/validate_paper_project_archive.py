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
"""Validate stable paper-project archives produced from timeline-paper builds."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path
from archive_timeline_paper_project import KNOWN_PROJECT_IDS, OUT_INDEX, PAPER_JSON, PROJECTS_ROOT, infer_project_id


REQUIRED_TIMELINE_PAPER_EXTS = {"json", "md", "pdf", "tex"}
COMMON_LATEX_FAILURE_MARKERS = [
    "<span",
    "</span>",
    "Misplaced &",
    "Missing argument",
    "Missing superscript",
    r"\textbackslash{}mathrm",
    r"\textbackslash{}mathbb",
    r"\textbackslash{}exists",
    r"\textbackslash{}Rightarrow",
    r"\textbackslash{}beta",
]

PVSNP_REQUIRED_PHRASES = [
    "P vs NP",
    "Formal Complexity Derivation",
    "Complexity Strategy",
    "Accumulated Proof Strategy Story",
]

PVSNP_FORBIDDEN_PHRASES = [
    "Yang-Mills",
    "mass gap",
    "Wilson",
    "Schur",
    "reflection positivity",
    "Schwinger",
    "Wightman",
    "gauge-invariant",
    "hairpin",
    "collar",
    "Formal Physics",
    "Physics And Maths",
    "Accumulated Physics",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def project_id_from_args(explicit: str) -> str:
    if clean_text(explicit):
        return infer_project_id({}, explicit)
    paper = load_json_object(PAPER_JSON)
    return infer_project_id(paper)


def assert_artifact(path_text: str) -> Path:
    path = repo_path(path_text, must_exist=True)
    require(path.is_file(), f"artifact is not a file: {path_text}")
    return path


def validate_artifact_map(artifacts: dict[str, Any], manifest: dict[str, Any]) -> dict[str, dict[str, str]]:
    require(isinstance(artifacts, dict) and artifacts, "manifest must contain project_artifacts")
    paper_artifacts = artifacts.get("timeline_paper", {})
    require(isinstance(paper_artifacts, dict), "timeline_paper artifacts must be a map")
    missing = sorted(REQUIRED_TIMELINE_PAPER_EXTS.difference(paper_artifacts))
    require(not missing, f"timeline_paper archive missing extensions: {', '.join(missing)}")
    for group, paths in artifacts.items():
        require(isinstance(paths, dict), f"{group} artifacts must be a map")
        for key, raw in paths.items():
            require(clean_text(raw), f"{group}.{key} path is empty")
            assert_artifact(str(raw))

    latex_sections = artifacts.get("timeline_latex_sections", {})
    require("tex" in latex_sections, "timeline_latex_sections/latest.tex was not archived")
    require("json" in latex_sections, "timeline_latex_sections/latest.json was not archived")
    project_root = repo_path(str(manifest.get("project_root")), must_exist=True)
    report_tex = project_root / "timeline_latex_sections" / "latest_report.tex"
    require(report_tex.exists(), f"missing report appendix TeX archive: {rel(report_tex)}")
    return artifacts  # type: ignore[return-value]


def validate_text_quality(tex_path: Path, target_id: str) -> None:
    tex = tex_path.read_text(encoding="utf-8")
    for marker in COMMON_LATEX_FAILURE_MARKERS:
        require(marker not in tex, f"archived TeX contains rendering failure marker: {marker}")
    if target_id == "p-vs-np-target":
        for phrase in PVSNP_REQUIRED_PHRASES:
            require(phrase in tex, f"P vs NP archived TeX missing required phrase: {phrase}")
        lowered = tex.lower()
        for phrase in PVSNP_FORBIDDEN_PHRASES:
            require(phrase.lower() not in lowered, f"P vs NP archive leaks cross-target phrase: {phrase}")


def validate_manifest(project_id: str) -> Path:
    manifest_path = PROJECTS_ROOT / project_id / "latest.json"
    require(manifest_path.exists(), f"missing paper-project manifest: {rel(manifest_path)}")
    manifest = load_json_object(manifest_path)
    require(manifest.get("status") == "paper_project_archive_ready", "manifest status must be paper_project_archive_ready")
    require(manifest.get("paper_project_id") == project_id, "manifest paper_project_id mismatch")
    require(clean_text(manifest.get("target_id")), "manifest target_id is empty")
    require(clean_text(manifest.get("title")), "manifest title is empty")

    if PAPER_JSON.exists():
        paper = load_json_object(PAPER_JSON)
        inferred = KNOWN_PROJECT_IDS.get(clean_text(paper.get("target_id")), "")
        if inferred == project_id:
            require(manifest.get("target_id") == paper.get("target_id"), "manifest target_id diverges from current latest paper")

    artifacts = validate_artifact_map(manifest.get("project_artifacts", {}), manifest)
    paper_tex = assert_artifact(artifacts["timeline_paper"]["tex"])
    validate_text_quality(paper_tex, str(manifest.get("target_id")))

    require(OUT_INDEX.exists(), f"missing paper-project index: {rel(OUT_INDEX)}")
    index = load_json_object(OUT_INDEX)
    indexed_ids = {entry.get("paper_project_id") for entry in index.get("projects", []) if isinstance(entry, dict)}
    require(project_id in indexed_ids, f"{project_id} missing from paper-project index")
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-project-id", default="", help="Stable paper-project id to validate; defaults to current latest paper target.")
    args = parser.parse_args()
    project_id = project_id_from_args(args.paper_project_id)
    manifest_path = validate_manifest(project_id)
    print(f"validated paper project archive: {rel(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
