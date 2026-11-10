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
"""Validate P vs NP negative tactic packets and fixtures."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"
FIXTURE_DIR = ROOT / "tests/fixtures/discovery_marathon"
ALLOWED_MODES = {
    "constructive_bridge",
    "proof_by_contradiction",
    "impossibility_theorem",
    "falsifier_search",
    "backtrack",
    "quarantine",
    "stop",
}
REQUIRED_REC_FIELDS = [
    "branch_id",
    "route_family",
    "tactic_mode",
    "reason_for_tactic",
    "exact_negation_or_method_class",
    "contradiction_carrier_or_no_go_family",
    "conflict_target",
    "escape_conditions",
    "proof_obligations",
    "branch_control_decision",
    "next_validation_handoff",
    "paper_contribution_potential",
]
DOMAIN_TERMS = [
    "sat",
    "circuit",
    "p/poly",
    "np",
    "beta",
    "q",
    "padding",
    "natural",
    "mcsp",
    "mktp",
    "proof",
    "advice",
    "oracle",
    "algebrization",
    "relativization",
]


def validate_recommendation(row: dict[str, Any], source: Path, index: int) -> None:
    for field in REQUIRED_REC_FIELDS:
        if not clean_text(row.get(field)):
            fail(f"{rel(source)} recommendation[{index}] missing {field}")
    if row.get("tactic_mode") not in ALLOWED_MODES:
        fail(f"{rel(source)} recommendation[{index}] invalid tactic_mode {row.get('tactic_mode')}")
    for list_field in ["escape_conditions", "proof_obligations"]:
        items = row.get(list_field)
        if not isinstance(items, list) or len([item for item in items if clean_text(item)]) < 2:
            fail(f"{rel(source)} recommendation[{index}] needs at least two {list_field}")
    text = clean_text(row).lower()
    if not any(term in text for term in DOMAIN_TERMS):
        fail(f"{rel(source)} recommendation[{index}] is not P vs NP-specific")
    if row.get("tactic_mode") in {"impossibility_theorem", "proof_by_contradiction"}:
        for marker in ["method", "conflict", "escape", "target"]:
            if marker not in text:
                fail(f"{rel(source)} recommendation[{index}] {row.get('tactic_mode')} lacks marker `{marker}`")
    if "assume p=np" in text and "local" not in text:
        fail(f"{rel(source)} recommendation[{index}] uses global assume P=NP rhetoric without local carrier")
    if row.get("tactic_mode") == "impossibility_theorem" and "escape" not in clean_text(row.get("paper_contribution_potential")).lower():
        fail(f"{rel(source)} recommendation[{index}] no-go theorem must preserve escape conditions")


def validate_payload(payload: dict[str, Any], source: Path) -> None:
    if payload.get("target_id") != "p-vs-np-target":
        fail(f"{rel(source)} target_id must be p-vs-np-target")
    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list) or not recommendations:
        fail(f"{rel(source)} needs nonempty recommendations")
    seen: set[str] = set()
    modes: set[str] = set()
    for index, row in enumerate(recommendations):
        if not isinstance(row, dict):
            fail(f"{rel(source)} recommendation[{index}] must be an object")
        validate_recommendation(row, source, index)
        rec_id = clean_text(row.get("recommendation_id") or row.get("branch_id"))
        if rec_id in seen:
            fail(f"{rel(source)} duplicate recommendation id {rec_id}")
        seen.add(rec_id)
        modes.add(clean_text(row.get("tactic_mode")))
    if source == REPORT and not modes.intersection({"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}):
        fail(f"{rel(source)} live report needs at least one decisive negative tactic recommendation")


def valid_fixture_paths() -> list[Path]:
    return [
        FIXTURE_DIR / "pvsnp_negative_tactic_valid.json",
        FIXTURE_DIR / "pvsnp_negative_tactic_blackbox_cap.json",
        FIXTURE_DIR / "pvsnp_negative_tactic_padding_projection.json",
        FIXTURE_DIR / "pvsnp_negative_tactic_natural_property.json",
        FIXTURE_DIR / "pvsnp_negative_tactic_mcsp_row.json",
        FIXTURE_DIR / "pvsnp_negative_tactic_proof_complexity.json",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(path) for path in args.paths] if args.paths else [REPORT]
    checked = 0
    for path in paths:
        if not path.exists():
            fail(f"missing {rel(path)}")
        validate_payload(load_json_object(path), path)
        checked += 1
    if not args.paths:
        for fixture in valid_fixture_paths():
            if fixture.exists():
                validate_payload(load_json_object(fixture), fixture)
                checked += 1
        invalid = FIXTURE_DIR / "pvsnp_negative_tactic_invalid.json"
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_payload(load_json_object(invalid), invalid)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail validation")
    print(f"validated {checked} P vs NP negative tactic packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
