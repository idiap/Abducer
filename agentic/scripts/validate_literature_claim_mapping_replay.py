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
"""Validate the generic claim-mapping and mapping-to-assimilation replay path."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.literature import (  # noqa: E402
    build_demo_literature_snapshot,
    build_theory_object_catalog,
    replay_literature_counterfactuals,
)


def main() -> int:
    snapshot = build_demo_literature_snapshot(target_id="literature-replay-self-check")
    catalog = build_theory_object_catalog(
        target_id=snapshot["target_id"],
        theory_state_digest=snapshot["theory_state_digest"],
        theory_objects=[
            {
                "theory_object_id": "concept.target-scope",
                "object_kind": "concept",
                "label": "Target scope",
                "match_terms": ["literature replay"],
                "scope_anchor": True,
            },
            {
                "theory_object_id": "concept.fixture-claim",
                "object_kind": "concept",
                "label": "Fixture claim",
                "match_terms": ["fixture claim"],
                "scope_anchor": False,
            },
        ],
    )
    first_source = snapshot["sources"][0]
    replay = replay_literature_counterfactuals(
        snapshot,
        theory_catalog=catalog,
        worlds=[
            {"world_id": "delete", "operation": "delete_source", "source_id": first_source["source_id"]},
            {"world_id": "none", "operation": "no_literature"},
            {"world_id": "superseded", "operation": "supersede_source", "source_id": first_source["source_id"]},
            {
                "world_id": "contradictory",
                "operation": "contradict_source",
                "source_id": first_source["source_id"],
                "contradictory_claim": "A counterexample contradicts the fixture claim.",
            },
            {
                "world_id": "coverage-null",
                "operation": "coverage_only_change",
                "coverage_limit": "Self-check provenance-only coverage qualification.",
                "expected_effect": "null",
            },
        ],
    )
    if replay["null_effect_world_ids"] != ["coverage-null"]:
        raise SystemExit("coverage-only world did not remain a semantic null")
    print("literature counterfactual replay: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
