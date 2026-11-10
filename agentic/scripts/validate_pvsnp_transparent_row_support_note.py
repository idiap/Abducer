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
"""Validate the focused TransparentRowSupport_N note."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_pvsnp_transparent_row_support_note import OUT_JSON, OUT_MD, OUT_TEX


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    note = load_json_object(OUT_JSON)
    require(note.get("status") == "transparent_row_support_note_ready", "note status is not ready")
    require(note.get("target_id") == "p-vs-np-target", "note target mismatch")
    require(note.get("paper_project_id") == "p-vs-np-transfer-obstruction-certificate", "note paper project mismatch")
    require("P != NP" in " ".join(note.get("non_claims", [])), "note must preserve P != NP non-claim")
    require("SAT outside P/poly" in " ".join(note.get("non_claims", [])), "note must preserve SAT/P-poly non-claim")
    fields = note.get("definition_fields", {})
    for key in [
        "visible_selector_code",
        "row_enumeration_or_scan_charge",
        "influence_closure",
        "row_expansion_charge",
        "same_theory_parser",
        "no_hidden_advice",
    ]:
        require(key in fields and clean_text(fields[key]), f"definition missing {key}")
    positive = note.get("positive_theorem", {})
    countermodel = note.get("countermodel_theorem", {})
    require("Gamma" in clean_text(positive.get("statement")), "positive theorem must state Gamma effect")
    require(len(positive.get("proof_spine", [])) >= 5, "positive theorem needs proof spine")
    require("private-row" in clean_text(countermodel.get("statement")) or "unread-enable" in clean_text(countermodel.get("statement")), "countermodel must state private-row/unread-enable mechanism")
    require(len(countermodel.get("countermodel_spine", [])) >= 4, "countermodel needs construction spine")
    require(len(note.get("examples_subsumed", [])) >= 5, "note must subsume selector examples")
    require("RealSATInfluenceRealizer_N" in clean_text(note.get("open_problems")), "note must name RealSATInfluenceRealizer_N")
    require("Do not add more selector classes" in clean_text(note.get("stop_rule")), "note must include anti-loop stop rule")
    for artifact in [OUT_MD, OUT_TEX]:
        require(artifact.exists(), f"missing {rel(artifact)}")
        text = artifact.read_text(encoding="utf-8")
        for phrase in ["TransparentRowSupport", "Gamma", "private-row", "Open Problems"]:
            require(phrase in text, f"{rel(artifact)} missing {phrase}")
    artifacts = note.get("artifacts", {})
    for key in ["json", "markdown", "tex"]:
        require(repo_path(artifacts.get(key, ""), must_exist=True).is_file(), f"artifact {key} is missing")
    pdf = clean_text(artifacts.get("pdf"))
    if pdf:
        require(repo_path(pdf, must_exist=True).is_file(), "pdf artifact path is invalid")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
