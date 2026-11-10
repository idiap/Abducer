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
"""Persist subgoal state transitions from the latest result atlas."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json


ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
STATE_DIR = ROOT / "agentic/state/subgoals"


def main() -> int:
    atlas = load_optional_json(ATLAS)
    target_id = clean_text(atlas.get("target_id"))
    if not target_id:
        raise SystemExit("missing target_id in result atlas")
    records = []
    for subgoal in atlas.get("subgoals", []):
        if not isinstance(subgoal, dict):
            continue
        records.append(
            {
                "transition_id": f"{subgoal.get('subgoal_id')}:{atlas.get('generated_utc')}",
                "target_id": target_id,
                "subgoal_id": subgoal.get("subgoal_id"),
                "status": subgoal.get("status"),
                "result_ids": subgoal.get("result_ids", []),
                "open_obligations": subgoal.get("open_obligations", []),
                "rationale": "Derived from validated result_subgoal_atlas; promotions require result evidence and demotions preserve open obligations.",
            }
        )
    payload = {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "source_atlas": rel(ATLAS),
        "subgoal_states": records,
    }
    out = STATE_DIR / f"{target_id}.json"
    write_json(out, payload)
    print(f"wrote {rel(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
