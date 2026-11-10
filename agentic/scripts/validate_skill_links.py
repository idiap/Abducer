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
"""Validate local links and every registered executable discovery route.

The registry is the cardinality authority.  The blind adjudicator is a real
operator because parent and synthesis preference must be sealed independently;
keeping a historical six-operator literal here would make the route validator
reject the very authority that the canonical workflow is required to consume.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from agentic_common import ROOT
from discovery_operator_registry import ROUTES_DOC_PATH, load_registry, render_routes


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_NAME_RE = re.compile(r"^---\s*\n.*?^name:\s*([^\n]+).*?^---\s*$", re.MULTILINE | re.DOTALL)


class LinkValidationError(ValueError):
    """Raised when a local skill or route contract is inconsistent."""


def _slug(text: str) -> str:
    text = re.sub(r"[`*_]", "", text.strip().lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def _validate_markdown(path: Path, expected_name: str) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_NAME_RE.search(text)
    if not match or match.group(1).strip() != expected_name:
        errors.append(f"{path}: front-matter name does not equal {expected_name!r}")
    headings = [_slug(item) for item in HEADING_RE.findall(text)]
    duplicates = sorted({item for item in headings if headings.count(item) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate semantic H2 sections: {duplicates}")
    anchors_by_file: dict[Path, set[str]] = {path: set(headings)}
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        file_part, _, anchor = target.partition("#")
        resolved = path if not file_part else (path.parent / file_part).resolve()
        if not resolved.exists():
            errors.append(f"{path}: broken local link {raw_target!r}")
            continue
        if anchor and resolved.suffix.lower() == ".md":
            if resolved not in anchors_by_file:
                linked_text = resolved.read_text(encoding="utf-8")
                anchors_by_file[resolved] = {_slug(item) for item in HEADING_RE.findall(linked_text)}
            if _slug(anchor) not in anchors_by_file[resolved]:
                errors.append(f"{path}: missing anchor {anchor!r} in {resolved}")
    return errors


def validate_registry_routes(registry: dict[str, Any]) -> list[str]:
    """Return all link, command, schema, and generated-doc parity errors."""

    errors: list[str] = []
    expected = {
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
        "canonical-causal-artifact-producer",
        "dynamic-symbolic-simulation-experimenter",
        "frontier-literature-assimilator",
        "formal-claim-producer",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "blind-conceptual-preference-adjudicator",
    }
    found = {item["operator_id"] for item in registry["operators"]}
    if found != expected:
        errors.append(f"operator set mismatch: missing={sorted(expected-found)}, extra={sorted(found-expected)}")
    if registry.get("parent_operator") != "reflective-conceptual-discovery":
        errors.append("reflective conceptual discovery must be the registry parent")
    experiment = next((item for item in registry["operators"] if item["operator_id"] == "dynamic-symbolic-simulation-experimenter"), {})
    if not experiment.get("conditional") or experiment.get("parent_operator") != registry.get("parent_operator"):
        errors.append("dynamic experiment operator must be a conditional child of reflective discovery")
    for operator in registry["operators"]:
        operator_id = operator["operator_id"]
        skill_path = ROOT / operator["skill_path"]
        if not skill_path.is_file():
            errors.append(f"{operator_id}: missing skill path {operator['skill_path']}")
        else:
            errors.extend(
                _validate_markdown(skill_path, skill_path.parent.name)
            )
        for field in ("entrypoint", "validator"):
            command = operator.get(field, [])
            if not isinstance(command, list) or len(command) < 2:
                errors.append(f"{operator_id}: invalid {field} command")
                continue
            script_parts = [part for part in command[1:] if isinstance(part, str) and part.endswith(".py")]
            if not script_parts or not (ROOT / script_parts[0]).is_file():
                errors.append(f"{operator_id}: unbound {field} path")
        for schema in [*operator.get("input_schemas", []), *operator.get("output_schemas", [])]:
            if not (ROOT / schema).is_file():
                errors.append(f"{operator_id}: missing schema {schema}")
        if not operator.get("required_consumers") or not operator.get("feedback_effect"):
            errors.append(f"{operator_id}: output consumption/feedback edge is not declared")
    expected_doc = render_routes(registry)
    if not ROUTES_DOC_PATH.exists():
        errors.append(f"missing generated route documentation {ROUTES_DOC_PATH}")
    elif ROUTES_DOC_PATH.read_text(encoding="utf-8") != expected_doc:
        errors.append("generated discovery operator documentation is stale")
    return errors


def main() -> int:
    try:
        registry = load_registry()
        errors = validate_registry_routes(registry)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(registry['operators'])} executable discovery skill routes and generated documentation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
