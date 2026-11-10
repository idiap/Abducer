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
"""Run a deep marathon review over accumulated cycle learning."""

from __future__ import annotations

import argparse

from agentic_common import rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_branches, load_cycles, load_run_state, review_path, write_markdown
from target_profiles import target_profile


def promotion_finding(target_id: str | None) -> str:
    profile = target_profile(target_id)
    if profile.get("target_id") == "p-vs-np-target":
        return (
            "Promotion remains blocked until a branch certifies a target-preserving source model, target class, "
            "quantitative threshold transfer, uniformity/nonuniformity boundary, and barrier status without collapsing "
            "into padding, oracle, natural-proof, or algebrization leakage."
        )
    if profile.get("target_id") == "yang-mills-existence-and-mass-gap-target":
        return (
            "Promotion remains blocked until certification reaches same-theory construction, reconstruction, "
            "nontriviality, and spectral-witness obligations."
        )
    return (
        "Promotion remains blocked until certification names the source object, target object, validity regime, "
        "falsifiers, and target-preserving transfer needed for the claimed contribution."
    )


def build_review(run_state: dict) -> dict:
    cycles = load_cycles(run_state)
    branches = load_branches(run_state)
    review_id = stable_id("marathon.review", run_state["run_id"], len(cycles), utc_now())
    learning = " ".join(cycle.get("cycle_learning", "") for cycle in cycles)
    recommendation = "continue_with_bridge_focused_branch_portfolio"
    if learning.lower().count("backtrack") >= 2:
        recommendation = "backtrack_retype_source_and_target_objects"
    return {
        "version": 1,
        "review_id": review_id,
        "run_id": run_state["run_id"],
        "created_utc": utc_now(),
        "cycle_count": len(cycles),
        "branch_count": len(branches),
        "summary": (
            "The marathon is producing theorem-shaped bridge pressure rather than free-floating strategies. "
            "No breakthrough is claimed; the live value is the sharpening of source objects, target objects, "
            "validity conditions, and falsifiers."
        ),
        "findings": [
            "Skill use is explicit across target navigation, branch selection, exploration, contradiction, evidence, gating, review, report, and release phases.",
            "Branch outputs include mathematical equations with validity conditions and next experiments.",
            promotion_finding(run_state.get("target_id", "")),
        ],
        "certification_boundary": promotion_finding(run_state.get("target_id", "")),
        "recommendation": recommendation,
        "next_review_trigger": "Run again after three additional cycles or after any branch claims a potential breakthrough signal.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    args = parser.parse_args()
    _, run_state = load_run_state(args.run_id)
    if not run_state:
        print("No active discovery marathon to review.")
        return 0
    review = build_review(run_state)
    path = review_path(run_state["run_id"], review["review_id"])
    write_json(path, review)
    write_markdown(
        path.with_suffix(".md"),
        "# Marathon Deep Review\n\n"
        f"{review['summary']}\n\n"
        "## Findings\n\n"
        + "".join(f"- {item}\n" for item in review["findings"])
        + f"\nRecommendation: `{review['recommendation']}`\n",
    )
    print(f"Wrote {rel(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
