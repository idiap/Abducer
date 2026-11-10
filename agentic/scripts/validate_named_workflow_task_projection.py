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

"""Validate that the visible named-workflow task registry is current."""

from __future__ import annotations

import json

from agentic_common import ROOT, fail
from generate_named_workflow_task_registry import OUTPUT, build_manifest


def main() -> int:
    expected = json.dumps(build_manifest(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
        fail(f"stale named workflow task projection: {OUTPUT.relative_to(ROOT)}")
    print("validated named workflow task projection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
