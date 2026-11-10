#!/usr/bin/env python3
"""Validate the portable Yang--Mills Codex skill bundle."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / ".agents" / "skills"
MANIFEST = ROOT / "skill_manifest.json"
CHECKSUMS = ROOT / "SKILL_CHECKSUMS.sha256"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path}")
    try:
        header = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError(f"unterminated YAML frontmatter: {path}") from exc
    values: dict[str, str] = {}
    for line in header.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def verify_checksums() -> None:
    expected: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        expected[rel] = digest
    actual: dict[str, str] = {}
    for path in sorted(p for p in SKILLS.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT).as_posix()
        actual[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        raise ValueError(
            f"checksum mismatch; missing={missing}, extra={extra}, changed={changed}"
        )


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    names: list[str] = []
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        agent_file = directory / "agents" / "openai.yaml"
        if not skill_file.is_file() or not agent_file.is_file():
            raise ValueError(f"incomplete skill directory: {directory}")
        metadata = frontmatter(skill_file)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != directory.name:
            raise ValueError(f"folder/frontmatter mismatch: {directory.name} != {name}")
        if not NAME_RE.fullmatch(name):
            raise ValueError(f"invalid public skill name: {name}")
        if not description:
            raise ValueError(f"missing description: {name}")
        names.append(name)

    expected_names = sorted(
        skill
        for phase in data["phase_order"]
        for skill in phase["skills"]
    )
    if len(names) != data["skill_count"] or names != expected_names:
        raise ValueError(
            f"manifest mismatch: found {len(names)} skills, expected {data['skill_count']}"
        )
    if len(names) != len(set(names)):
        raise ValueError("duplicate skill names")
    if data["orchestrator"] not in names:
        raise ValueError("orchestrator is absent")

    verify_checksums()
    print(json.dumps({
        "valid": True,
        "skill_count": len(names),
        "orchestrator": data["orchestrator"],
        "repo_install_root": data["repo_install_root"],
        "skills": names,
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"bundle validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

