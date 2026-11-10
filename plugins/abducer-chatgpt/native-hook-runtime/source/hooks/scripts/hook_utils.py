#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Shared deterministic hook helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TRACE_DIR = ROOT / "agentic" / "traces" / "hook_runs"
DESTRUCTIVE_COMMAND_MARKERS = ("rm -rf", "git reset --hard", "git checkout --", "mkfs", "dd if=")
PROTECTED_PREFIXES = ("agentic/", "registry/", "hooks/", "skills/control-plane/looper-", "docs/looper-")


def read_payload() -> dict:
    text = sys.stdin.read().strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
    return payload if isinstance(payload, dict) else {"payload": payload}


def emit(**payload: object) -> None:
    print(json.dumps(payload, sort_keys=True))


def trace(hook_name: str, payload: dict, result: dict) -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    path = TRACE_DIR / f"latest-{hook_name}.json"
    path.write_text(json.dumps({"hook": hook_name, "payload": payload, "result": result}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def protected_path(raw: str) -> bool:
    # Preserve the original docs/looper-* protection after thematic relocation.
    if str(raw).startswith("docs/integrations/looper-"):
        raw = str(raw).replace("docs/integrations/", "docs/", 1)
    return any(str(raw).startswith(prefix) for prefix in PROTECTED_PREFIXES)


def has_evidence_marker(payload: dict) -> bool:
    text = json.dumps(payload, sort_keys=True).lower()
    return "lint-" in text or "todo" in text or "decision" in text or "evidence" in text
