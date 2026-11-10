#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Resolve a checkout-backed plugin skill without writing research state.

ABDUCER_ROOT or --root selects a checkout explicitly. Otherwise the nearest
Abducer ancestor of cwd wins. The plugin cache cannot substitute for a runtime:
it has neither the project manifest nor the canonical source skill tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tomllib

PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def resolve(
    skill: str, explicit_root: str | None = None, *, workflow: bool = False
) -> dict[str, str]:
    """Validate identity, source containment and source version before routing."""
    inventory = "workflows.json" if workflow else "source-skills.json"
    rows = json.loads((PLUGIN_ROOT / inventory).read_text())[
        "workflows" if workflow else "skills"
    ]
    row = next(
        (row for row in rows if row["id" if workflow else "name"] == skill), None
    )
    if row is None:
        raise ValueError(
            f"Unknown {'normalized workflow' if workflow else 'public Abducer skill'}: {skill}"
        )
    selected = explicit_root or os.environ.get("ABDUCER_ROOT")
    cwd = Path.cwd()
    candidates = [Path(selected).expanduser()] if selected else [cwd, *cwd.parents]
    for candidate in candidates:
        root = candidate.resolve()
        manifest = root / "pyproject.toml"
        if not manifest.is_file():
            continue
        try:
            project = tomllib.loads(manifest.read_text()).get("project", {})
        except (tomllib.TOMLDecodeError, OSError):
            continue
        if project.get("name") != "abducer-discovery-runtime":
            continue
        source_name = row["owner"] if workflow else row["source"]
        source = (root / source_name).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError(f"Missing or escaped canonical source: {source_name}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != row["owner_sha256" if workflow else "sha256"]:
            raise ValueError(
                "Plugin and checkout skill versions differ. Regenerate and reinstall "
                "the plugin from this checkout; see docs/integrations/agent-plugins.md."
            )
        result = {"root": str(root), "skill_file": str(source), "sha256": digest}
        if workflow:
            descriptor = (root / row["descriptor"]).resolve()
            if not descriptor.is_relative_to(root) or not descriptor.is_file():
                raise ValueError("Missing or escaped canonical workflow descriptor")
            if (
                hashlib.sha256(descriptor.read_bytes()).hexdigest()
                != row["descriptor_sha256"]
            ):
                raise ValueError(
                    "Plugin and checkout workflow versions differ; regenerate and reinstall the plugin"
                )
            result.update(workflow_file=str(descriptor), workflow_id=row["id"])
        return result
    raise ValueError(
        "No Abducer checkout found. Set ABDUCER_ROOT or pass --root to a writable "
        "Abducer checkout, then provision its runtime with uv sync --locked."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill")
    selection.add_argument("--workflow", help="Canonical normalized workflow ID")
    parser.add_argument("--root", help="Explicit Abducer checkout path")
    args = parser.parse_args()
    try:
        result = resolve(
            args.workflow or args.skill, args.root, workflow=bool(args.workflow)
        )
    except (OSError, ValueError, KeyError) as exc:
        print(f"Abducer setup required: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
