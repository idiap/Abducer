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

"""Shared helpers for Abducer's Looper-style control plane.

The control plane intentionally uses only the Python standard library. Files
with a ``.yaml`` extension are written as JSON-compatible YAML so the first
integrated slice stays dependency-free while remaining easy to replace with a
full YAML parser later.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def rel(path: Path | str) -> str:
    """Return a stable repo-relative path when possible."""

    target = Path(path)
    try:
        return str(target.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(target)


def fail(message: str) -> None:
    """Print a validation error and exit non-zero."""

    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json_like(path: Path) -> Any:
    """Load JSON or JSON-compatible YAML from ``path``."""

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {rel(path)}: {exc}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"{rel(path)} is not JSON-compatible YAML: {exc}")


def load_json_object(path: Path) -> dict[str, Any]:
    """Load a JSON object and reject non-object payloads."""

    payload = load_json_like(path)
    if not isinstance(payload, dict):
        fail(f"{rel(path)} must contain an object")
    return payload


def load_json_array(path: Path) -> list[Any]:
    """Load a JSON array and reject non-array payloads."""

    payload = load_json_like(path)
    if not isinstance(payload, list):
        fail(f"{rel(path)} must contain an array")
    return payload


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_path(raw: str, *, base: Path = ROOT, must_exist: bool = False) -> Path:
    """Resolve a safe repo-relative path."""

    if not isinstance(raw, str) or not raw.strip():
        fail("empty repo-relative path")
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(f"invalid repo-relative path: {raw}")
    path = base / candidate
    if must_exist and not path.exists():
        fail(f"missing path: {raw}")
    return path


def clean_text(value: Any) -> str:
    """Normalize arbitrary text for stable comparisons."""

    return " ".join(str(value or "").strip().split())


def slugify(value: Any) -> str:
    """Create a compact filesystem-safe slug."""

    text = clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "target"


def stable_id(prefix: str, *parts: Any) -> str:
    """Create a short stable ID from content."""

    payload = json.dumps([str(part) for part in parts], sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}.{digest}"


def ensure_list(value: Any) -> list[Any]:
    """Return ``value`` if it is a list, otherwise an empty list."""

    return value if isinstance(value, list) else []


def ensure_dict(value: Any) -> dict[str, Any]:
    """Return ``value`` if it is a dict, otherwise an empty dict."""

    return value if isinstance(value, dict) else {}


_FENCE_RE = re.compile(r"```yaml\s*(.*?)```", re.DOTALL)
_TOP_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "''", '""'}:
        return ""
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_simple_yaml_block(block: str) -> dict[str, Any]:
    """Parse the small top-level YAML subset used in KB statement blocks."""

    data: dict[str, Any] = {}
    current_list: str | None = None
    current_multiline: str | None = None
    multiline_lines: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            if current_multiline:
                multiline_lines.append("")
            continue
        if current_multiline:
            if not line.startswith(" ") and _TOP_KEY_RE.match(stripped):
                data[current_multiline] = "\n".join(multiline_lines).strip()
                current_multiline = None
                multiline_lines = []
            else:
                multiline_lines.append(stripped)
                continue
        if current_list and stripped.startswith("- "):
            data.setdefault(current_list, []).append(_parse_scalar(stripped[2:]))
            continue
        match = _TOP_KEY_RE.match(stripped)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        current_list = None
        if value in {"|", ">"}:
            current_multiline = key
            multiline_lines = []
            continue
        parsed = _parse_scalar(value)
        data[key] = parsed
        if value == "":
            current_list = key
            data[key] = []
    if current_multiline:
        data[current_multiline] = "\n".join(multiline_lines).strip()
    return data


def parse_kb_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """Extract statement cards from ``KB/*.kb.md`` fenced YAML blocks."""

    if not kb_path.exists():
        fail(f"missing KB file: {rel(kb_path)}")
    text = kb_path.read_text(encoding="utf-8")
    statements: dict[str, dict[str, Any]] = {}
    for block in _FENCE_RE.findall(text):
        item = parse_simple_yaml_block(block)
        statement_id = clean_text(item.get("id"))
        if not statement_id:
            continue
        item["id"] = statement_id
        item.setdefault("kind", "statement")
        item.setdefault("status", "tentative")
        item.setdefault("depends_on", [])
        if not isinstance(item["depends_on"], list):
            item["depends_on"] = []
        item.setdefault("source_ids", [])
        if not isinstance(item["source_ids"], list):
            item["source_ids"] = []
        statements[statement_id] = item
    return statements


def kb_ref_from_path(kb_path: Path) -> str:
    """Return the canonical artifact slug for a KB path."""

    name = kb_path.name
    if name.endswith(".kb.md"):
        return name[: -len(".kb.md")]
    return kb_path.stem


def load_optional_json(path: Path) -> dict[str, Any]:
    """Load an optional JSON object, returning an empty object when absent."""

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_optional_json_list(path: Path) -> list[Any]:
    """Load an optional JSON list, returning an empty list when absent."""

    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return payload if isinstance(payload, list) else []


def parse_phyp_file(path: Path) -> list[dict[str, Any]]:
    """Parse the compact top-level hypothesis records used in phyp YAML files."""

    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    active_list: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- id:"):
            if current:
                rows.append(current)
            current = {"id": clean_text(stripped.split(":", 1)[1])}
            active_list = None
            continue
        if current is None:
            continue
        if active_list and stripped.startswith("- "):
            current.setdefault(active_list, []).append(_parse_scalar(stripped[2:]))
            continue
        match = _TOP_KEY_RE.match(stripped)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        if value == "":
            current[key] = []
            active_list = key
            continue
        active_list = None
        current[key] = _parse_scalar(value)
    if current:
        rows.append(current)
    return rows


def iter_skill_dirs() -> list[Path]:
    """Return all local Abducer skill directories."""

    return sorted(path.parent for path in (ROOT / "skills").glob("*/*/SKILL.md"))


def skill_name_from_dir(path: Path) -> str:
    """Return a stable skill name from a skill directory."""

    return path.name


def skill_dir_by_name(name: str) -> Path | None:
    """Find a local skill directory by stable skill name."""

    for path in iter_skill_dirs():
        if skill_name_from_dir(path) == name:
            return path
    return None


def read_skill_description(path: Path) -> str:
    """Extract a compact skill description from SKILL.md frontmatter."""

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return ""
    text = skill_md.read_text(encoding="utf-8-sig")
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    return clean_text(match.group(1)) if match else ""


def collect_file_evidence(paths: list[str]) -> list[str]:
    """Return existing file evidence strings for paths."""

    evidence = []
    for raw in paths:
        path = ROOT / raw
        if path.exists():
            evidence.append(f"file:{raw}")
    return evidence
