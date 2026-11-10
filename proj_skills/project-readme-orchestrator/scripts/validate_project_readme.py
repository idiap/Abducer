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
"""Validate Abducer's README as a navigable, truthful project front door."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

LOCAL_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _local_target(base: Path, raw: str) -> Path | None:
    target = raw.strip().strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    return (base / target.split("#", 1)[0]).resolve()


def validate_readme(repo: Path, readme_path: Path | None = None) -> dict[str, Any]:
    repo = repo.resolve()
    readme = (readme_path if readme_path and readme_path.is_absolute() else repo / (readme_path or "README.md")).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not readme.is_file():
        return {"status": "fail", "readme": str(readme), "checks": {}, "errors": ["README file is missing."], "warnings": []}
    text = readme.read_text(encoding="utf-8")

    if not re.search(r"^#\s+Abducer\b", text, re.MULTILINE):
        errors.append("README must identify Abducer in its H1 heading.")
    required = {
        "project goal": "## Goal",
        "research loop": "## Current Research Loop",
        "documentation index": "docs/README.md",
        "architecture documentation": "docs/architecture/architecture.md",
        "skill documentation": "docs/reference/skills.md",
        "knowledge-base surface": "KB/",
        "proof-hypothesis surface": "phyp/",
        "scientific skill surface": "skills/",
    }
    for label, fragment in required.items():
        if fragment not in text:
            errors.append(f"README is missing {label}: {fragment!r}.")

    broken: set[str] = set()
    for raw in LOCAL_LINK_RE.findall(text):
        target = _local_target(readme.parent, raw)
        if target is not None and not target.exists():
            broken.add(raw)
    errors.extend(f"Broken local link: {target}" for target in sorted(broken))

    headings = len(re.findall(r"^##\s+", text, re.MULTILINE))
    if headings > 18:
        warnings.append(f"README has {headings} H2 sections; consider moving specialist detail under docs/.")
    if "proj_skills/" not in text:
        warnings.append("README does not yet point readers to the optional project-support skill pack.")

    return {
        "status": "pass" if not errors else "fail",
        "readme": str(readme),
        "checks": {"local_links_checked": len(LOCAL_LINK_RE.findall(text)), "h2_sections": headings},
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--readme", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    result = validate_readme(args.repo, args.readme)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
