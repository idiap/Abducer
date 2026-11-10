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
"""Quick-validate repository-local SKILL.md and agents/openai.yaml contracts."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

from agentic_common import ROOT, iter_skill_dirs, rel


SKILLS_ROOT = ROOT / "skills"
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
TOP_LEVEL_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
INTERFACE_FIELD_RE = re.compile(
    r"^\s{2,}(display_name|short_description|default_prompt):\s*(.*?)\s*$"
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}


def _scalar(raw: str) -> str:
    """Parse the quoted or plain scalar subset used by local skill metadata."""

    value = raw.strip()
    if value[:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
        return parsed if isinstance(parsed, str) else value
    return value


def _frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, ["SKILL.md needs a leading YAML frontmatter block"]
    values: dict[str, str] = {}
    errors: list[str] = []
    for line_number, raw_line in enumerate(match.group(1).splitlines(), start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#") or raw_line[:1].isspace():
            continue
        field = TOP_LEVEL_RE.match(raw_line)
        if not field:
            errors.append(f"line {line_number}: malformed top-level frontmatter")
            continue
        key, raw_value = field.group(1), field.group(2) or ""
        if key in values:
            errors.append(f"line {line_number}: duplicate frontmatter key {key!r}")
        values[key] = _scalar(raw_value)
    unexpected = sorted(set(values) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(f"unexpected frontmatter keys: {', '.join(unexpected)}")
    return values, errors


def _interface(text: str) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    errors: list[str] = []
    in_interface = False
    saw_interface = False
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        top = TOP_LEVEL_RE.match(raw_line)
        if top:
            in_interface = top.group(1) == "interface"
            saw_interface = saw_interface or in_interface
            continue
        if not in_interface or not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        field = INTERFACE_FIELD_RE.match(raw_line)
        if not field:
            continue
        key, raw_value = field.groups()
        if key in values:
            errors.append(f"line {line_number}: duplicate interface field {key!r}")
        values[key] = _scalar(raw_value)
    if not saw_interface:
        errors.append("agents/openai.yaml needs an interface mapping")
    return values, errors


def validate_skill(skill_dir: Path) -> list[str]:
    """Return deterministic metadata errors for one repository-local skill."""

    skill_dir = skill_dir.resolve()
    errors: list[str] = []
    try:
        skill_dir.relative_to(SKILLS_ROOT.resolve())
    except ValueError:
        return [f"{skill_dir} is outside {SKILLS_ROOT.resolve()}"]
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{rel(skill_md)} is missing"]

    values, parse_errors = _frontmatter(skill_md.read_text(encoding="utf-8-sig"))
    errors.extend(parse_errors)
    name = values.get("name", "").strip()
    description = values.get("description", "").strip()
    if not name:
        errors.append("frontmatter name is required")
    elif not NAME_RE.fullmatch(name):
        errors.append("frontmatter name must be lowercase hyphen-case")
    elif len(name) > 64:
        errors.append("frontmatter name exceeds 64 characters")
    if name and name != skill_dir.name:
        errors.append(f"frontmatter name {name!r} does not match directory {skill_dir.name!r}")
    if not description:
        errors.append("frontmatter description is required")
    elif len(description) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")
    if "<" in description or ">" in description:
        errors.append("frontmatter description cannot contain angle brackets")

    agent_path = skill_dir / "agents/openai.yaml"
    if not agent_path.is_file():
        errors.append(f"{rel(agent_path)} is missing")
        return errors
    interface, interface_errors = _interface(agent_path.read_text(encoding="utf-8-sig"))
    errors.extend(interface_errors)
    for field in ("display_name", "short_description", "default_prompt"):
        if not interface.get(field, "").strip():
            errors.append(f"agents/openai.yaml interface.{field} is required")
    short_description = interface.get("short_description", "").strip()
    if short_description and not 25 <= len(short_description) <= 64:
        errors.append("interface.short_description must contain 25-64 characters")
    default_prompt = interface.get("default_prompt", "")
    if name and f"${name}" not in default_prompt:
        errors.append(f"interface.default_prompt must mention ${name}")
    return errors


def _resolve_skill_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path.parent if path.name == "SKILL.md" else path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill directories or SKILL.md paths; defaults to every local skill.",
    )
    args = parser.parse_args(argv)
    skill_dirs = [_resolve_skill_path(raw) for raw in args.skills] or iter_skill_dirs()
    failures = 0
    for skill_dir in skill_dirs:
        for error in validate_skill(skill_dir):
            failures += 1
            print(f"ERROR: {rel(skill_dir)}: {error}", file=sys.stderr)
    if failures:
        print(f"repository skill quick validation found {failures} error(s)", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} repository-local skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
