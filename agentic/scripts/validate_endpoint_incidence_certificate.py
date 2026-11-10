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
"""Validate the endpoint kappa_4 incidence certificate."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel
from build_endpoint_incidence_certificate import OUT_JSON, OUT_MD


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    for field in [
        "target_id",
        "status",
        "source_cycle_ids",
        "symbolic_dominance_certificate",
        "seven_point_stencil_verification",
        "incidence_table_schema",
        "next_work_queue",
        "paper_claim_boundary",
    ]:
        require(report.get(field), f"{rel(OUT_JSON)} missing {field}")
    require("geometry_pending" in clean_text(report["status"]), "status must honestly mark geometry pending")
    require(len(report["source_cycle_ids"]) >= 3, "certificate needs at least three source cycles")
    cert = report["symbolic_dominance_certificate"]
    dominance = cert.get("dominance_functional", {})
    require("2 B_12" in clean_text(dominance.get("formula")), "dominance formula must include B_12 term")
    require("[D_v]_+" in clean_text(dominance.get("dangerous_part")), "certificate must identify positive dangerous part")
    lower = cert.get("certified_lower_bound", {})
    require("M_G" in clean_text(lower.get("formula")), "lower bound must compare against M_G")
    require("C_col" in clean_text(lower.get("formula")), "lower bound must include color factor")
    stencil = report["seven_point_stencil_verification"]
    require(stencil.get("normalizes_fourth_derivative") is True, "stencil must normalize fourth derivative")
    require(stencil.get("signed_error_coefficient") == "-7/240", "stencil signed error coefficient must be -7/240")
    require("7/240" in clean_text(stencil.get("absolute_error_bound")), "stencil must expose absolute error bound")
    rows = report["incidence_table_schema"]
    require(len(rows) >= 4, "incidence schema needs endpoint classes")
    for row in rows:
        joined = clean_text(row)
        for token in ["B_12,v", "B_13,v", "B_23,v", "D_v"]:
            require(token in joined, f"incidence row missing {token}")
        require(row.get("current_status") == "geometry_not_yet_enumerated", "schema must not pretend geometry is computed")
    queue = report["next_work_queue"]
    require([item.get("rank") for item in queue] == [1, 2, 3], "next work queue must have ranks 1,2,3")
    for item in queue:
        require(clean_text(item.get("payoff")) and clean_text(item.get("stop_when")), "queue items need payoff and stop condition")
        require("next-experiment-queue-ranker" in item.get("required_skills", []), "queue item must use ranker")
    boundary = report["paper_claim_boundary"]
    require("not_claimable_yet" in boundary, "claim boundary must include non-claim")
    require("B-table" in clean_text(boundary.get("not_claimable_yet")), "non-claim must mention missing B-table")
    require(OUT_MD.exists(), f"missing {rel(OUT_MD)}")
    text = OUT_MD.read_text(encoding="utf-8")
    for phrase in ["Endpoint Incidence Certificate", "Dominance Functional", "Certified Lower Bound", "Seven-Point Stencil", "Claim Boundary"]:
        require(phrase in text, f"{rel(OUT_MD)} missing `{phrase}`")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
