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
"""Validate the structure and Abducer-specific hygiene of project-support skills."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

FORBIDDEN = {
    "donor project name": re.compile(r"\b(?:Rover|SVA)\b", re.I),
    "donor trace path": re.compile(r"(?:\.rover|\brover/)"),
    "donor product": re.compile(r"Spectra Reasoner", re.I),
    "donor generated artifact": re.compile(r"generated_assertions\.sv", re.I),
    "external CDN": re.compile(r"jsdelivr", re.I),
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"\'')
    return result


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills = sorted(path.parent for path in root.glob("*/SKILL.md"))
    catalog_path = root / "catalog.yaml"
    catalog: dict[str, object] = {}
    if not catalog_path.is_file():
        errors.append("catalog.yaml is missing")
    else:
        try:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"catalog.yaml is invalid JSON-compatible YAML: {exc}")
    catalog_ids = catalog.get("skills", []) if isinstance(catalog, dict) else []
    if not isinstance(catalog_ids, list) or not all(isinstance(item, str) for item in catalog_ids):
        errors.append("catalog.yaml skills must be a list of skill IDs")
        catalog_ids = []
    actual_ids = [path.name for path in skills]
    if sorted(catalog_ids) != actual_ids:
        missing = sorted(set(actual_ids) - set(catalog_ids))
        stale = sorted(set(catalog_ids) - set(actual_ids))
        errors.append(f"catalog mismatch: missing={missing}, stale={stale}")
    index = (root / "INDEX.md").read_text(encoding="utf-8") if (root / "INDEX.md").is_file() else ""
    if not index:
        errors.append("INDEX.md is missing")

    for skill_dir in skills:
        skill_file = skill_dir / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        metadata = _frontmatter(text)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{skill_file}: frontmatter name must match directory")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{skill_file}: invalid skill name")
        if not description or len(description) > 1024:
            errors.append(f"{skill_file}: description must be 1..1024 characters")
        if f"({skill_dir.name}/SKILL.md)" not in index:
            errors.append(f"INDEX.md does not link {skill_dir.name}")

        agent = skill_dir / "agents" / "openai.yaml"
        if not agent.is_file():
            errors.append(f"{skill_dir}: agents/openai.yaml is missing")
        else:
            agent_text = agent.read_text(encoding="utf-8")
            for field in ("display_name:", "short_description:", "default_prompt:"):
                if field not in agent_text:
                    errors.append(f"{agent}: missing {field[:-1]}")
            short_match = re.search(r'^\s*short_description:\s*["\']?(.+?)["\']?\s*$', agent_text, re.MULTILINE)
            if short_match and not 25 <= len(short_match.group(1).rstrip('"\'')) <= 64:
                errors.append(f"{agent}: short_description must be 25..64 characters")
            if f"${name}" not in agent_text:
                errors.append(f"{agent}: default prompt must mention ${name}")

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        # Python may create bytecode while this same pack is under test. Distribution
        # tooling excludes it; archive-origin debris remains a hard error.
        if path.name.startswith("._") or "__MACOSX" in rel.parts:
            errors.append(f"archive debris: {rel}")
        if path.name == "__pycache__" or path.suffix == ".pyc":
            continue
        if not path.is_file() or path in {root / "PROVENANCE.md", Path(__file__).resolve()}:
            continue
        if path.suffix in {".md", ".py", ".yaml", ".yml", ".json"}:
            text = path.read_text(encoding="utf-8")
            for label, pattern in FORBIDDEN.items():
                if pattern.search(text):
                    errors.append(f"{rel}: contains {label}")
            if path.suffix == ".md":
                for raw in LINK_RE.findall(text):
                    target = raw.strip().strip("<>")
                    if target.startswith(("#", "http://", "https://", "mailto:")) or not target:
                        continue
                    resolved = (path.parent / target.split("#", 1)[0]).resolve()
                    if not resolved.exists():
                        errors.append(f"{rel}: broken local link {raw}")
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"{rel}: Python syntax error: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print("project-support skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    root = args.root.resolve()
    catalog = json.loads((root / "catalog.yaml").read_text(encoding="utf-8"))
    print(f"validated {len(catalog['skills'])} catalogued project-support skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
