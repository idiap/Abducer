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
"""Validate target-scoped proof learning ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, slugify


LEDGER_ROOT = ROOT / "agentic/reports/proof_learning/targets"
SCHEMA = ROOT / "agentic/spec/proof_inference_learning_event.schema.json"


def require_nonempty(value: Any, source: Path, field: str) -> None:
    if not clean_text(value):
        fail(f"{rel(source)} missing {field}")


def validate_ledger(path: Path) -> int:
    payload = load_json_object(path)
    target_id = clean_text(payload.get("target_id"))
    require_nonempty(target_id, path, "target_id")
    if path.parent.name != slugify(target_id):
        fail(f"{rel(path)} path target slug does not match target_id {target_id}")
    events = payload.get("events")
    if not isinstance(events, list):
        fail(f"{rel(path)} events must be a list")
    schema = load_json_object(SCHEMA)
    allowed = set(schema["allowed_event_types"])
    seen: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            fail(f"{rel(path)} events must contain objects")
        for field in schema["required_fields"]:
            require_nonempty(event.get(field), path, f"event.{field}")
        if clean_text(event.get("target_id")) != target_id:
            fail(f"{rel(path)} mixes target_id {event.get('target_id')} into {target_id}")
        event_id = clean_text(event.get("event_id"))
        if event_id in seen:
            fail(f"{rel(path)} duplicate event_id {event_id}")
        seen.add(event_id)
        if clean_text(event.get("epistemic_status")) not in allowed:
            fail(f"{rel(path)} invalid event epistemic_status {event.get('epistemic_status')}")
        if not isinstance(event.get("evidence"), list) or not event.get("evidence"):
            fail(f"{rel(path)} event {event_id} missing evidence")
    for field in ["transfer_substance_rules", "branch_routing_rules", "required_certificates", "demoted_generalizations"]:
        if not isinstance(payload.get(field), list):
            fail(f"{rel(path)} {field} must be a list")
    require_nonempty(payload.get("validation_handoff"), path, "validation_handoff")
    return len(events)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(raw) for raw in args.paths] if args.paths else sorted(LEDGER_ROOT.glob("*/latest.json"))
    if not paths:
        fail("no proof learning ledger reports found; run agentic/scripts/build_proof_learning_ledger.py")
    total = sum(validate_ledger(path) for path in paths)
    print(f"validated {total} proof learning event(s) across {len(paths)} ledger(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
