#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate controlled-iteration release reports."""

from __future__ import annotations

from agentic_common import ROOT, fail, rel


REQUIRED_SECTIONS = [
    "## Target",
    "## Workflow",
    "## Evidence",
    "## Dependency Status",
    "## Drift",
    "## Rollback",
    "## Open Blockers",
    "## Decision",
]


def main() -> int:
    paths = sorted((ROOT / "agentic" / "reports" / "releases").glob("ITER-*.md"))
    if not paths:
        fail("no release reports found")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                fail(f"{rel(path)} missing release section: {section}")
        if "Decision: " not in text:
            fail(f"{rel(path)} missing explicit Decision line")
    print(f"validated {len(paths)} release reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
